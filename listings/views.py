from django.urls import reverse

from django.http import JsonResponse

# Create your views here
from django.views.generic import DetailView
from .models import *


from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Restaurant, CarRentalAgency
import json


@require_POST
def update_rating(request, listing_type, slug):
    # Map URL patterns to models
    model_map = {
        "hotels": Hotel,
        "restaurants": Restaurant,
        "car-rental-agencies": CarRentalAgency,
    }

    try:
        # Parse the JSON data
        data = json.loads(request.body)
        new_rating = float(data.get("rating"))

        # Validate rating
        if not 1 <= new_rating <= 5:
            return JsonResponse({"error": "Invalid rating value"}, status=400)

        # Get the model class based on the listing type
        Model = model_map.get(listing_type)
        if not Model:
            return JsonResponse({"error": "Invalid listing type"}, status=400)

        # Get the object
        obj = get_object_or_404(Model, slug=slug)

        # Update the rating
        obj.rating = new_rating
        obj.save()

        # Return the new average rating
        return JsonResponse({"status": "success", "average_rating": float(obj.rating)})

    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Add this mixin to your detail views
class ListingDetailMixin:
    @property
    def model_name(self):
        return self.model.__name__


# Update your detail views
class HotelDetailView(ListingDetailMixin, DetailView):
    model = Hotel
    template_name = "listings/hotel_detail.html"


from django.db.models import Prefetch


class RestaurantDetailView(ListingDetailMixin, DetailView):
    model = Restaurant
    template_name = "listings/restaurant_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define category mapping
        category_mapping = {
            "main": "main",  # Maps to your model's CATEGORY_CHOICES
            "appetizers": "appetizer",
            "desserts": "dessert",
            "beverages": "beverage",
        }

        # Initialize menu_items dictionary
        menu_items = {}

        # Fetch and organize items by category
        for display_name, model_name in category_mapping.items():
            menu_items[display_name] = self.object.menu_items.filter(
                category=model_name, is_available=True
            ).select_related("restaurant")

        context["menu_items"] = menu_items
        return context


class CarRentalAgencyDetailView(ListingDetailMixin, DetailView):
    model = CarRentalAgency
    template_name = "listings/car_rental_agency_detail.html"


def hotel_list(request):
    data_url = reverse("hotel_list_api")
    hotels = list(Hotel.objects.values("address"))
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل الفنادق",
            "data_url": data_url,
            "min_price": 5000,
            "max_price": 50000,
            "price_step": 1000,
            "locations": hotels,
        },
    )


def restaurant_list(request):
    data_url = reverse("restaurant_list_api")
    restaurants = list(Restaurant.objects.values("address"))
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل المطاعم",
            "data_url": data_url,
            "min_price": 500,
            "max_price": 5000,
            "price_step": 100,
            "locations": restaurants,
        },
    )


def car_rental_agency_list(request):
    data_url = reverse("car_rental_agency_list_api")
    agencies = list(CarRentalAgency.objects.values("address"))
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل وكالات كراء السيارات",
            "data_url": data_url,
            "min_price": 2000,
            "max_price": 100000,
            "price_step": 1000,
            "locations": agencies,
        },
    )


def hotel_list_api(request):
    hotels = list(
        Hotel.objects.values(
            "id", "name", "address", "price_per_night", "rating", "main_image", "slug"
        )
    )
    return JsonResponse(hotels, safe=False)


def restaurant_list_api(request):
    restaurants = list(
        Restaurant.objects.values(
            "id", "name", "address", "price_range", "rating", "main_image", "slug"
        )
    )
    return JsonResponse(restaurants, safe=False)


def car_rental_agency_list_api(request):
    agencies = list(
        CarRentalAgency.objects.values(
            "id", "name", "address", "price_per_day", "rating", "main_image", "slug"
        )
    )
    return JsonResponse(agencies, safe=False)


from .forms import get_reservation_form


def make_reservation(request, listing_type, slug):
    if listing_type == "hotels":
        listing = get_object_or_404(Hotel, slug=slug)
    elif listing_type == "restaurants":
        listing = get_object_or_404(Restaurant, slug=slug)
    elif listing_type == "car-rental-agencies":
        listing = get_object_or_404(CarRentalAgency, slug=slug)
    else:
        raise ValueError("Invalid listing type")

    FormClass = get_reservation_form(
        listing_type,
        hotel=listing if listing_type == "hotels" else None,
        restaurant=listing if listing_type == "restaurants" else None,
        agency=listing if listing_type == "car-rental-agencies" else None,
    )

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect("reservation_confirmation", reservation.id)
    else:
        form = FormClass()

    return render(
        request,
        "reservations/reservation_form.html",
        {"form": form, "listing_type": listing_type, "listing": listing},
    )


def reservation_confirmation(request, reservation_id):
    reservation = (
        get_object_or_404(
            HotelReservation.objects.select_related("hotel").prefetch_related(
                "reservationroom_set__room"
            ),
            pk=reservation_id,
        )
        if HotelReservation.objects.filter(pk=reservation_id).exists()
        else (
            get_object_or_404(
                RestaurantReservation.objects.select_related(
                    "restaurant"
                ).prefetch_related("reservationmenuitem_set__menu_item"),
                pk=reservation_id,
            )
            if RestaurantReservation.objects.filter(pk=reservation_id).exists()
            else get_object_or_404(
                CarReservation.objects.select_related("agency").prefetch_related(
                    "reservationcar_set__car"
                ),
                pk=reservation_id,
            )
        )
    )

    return render(
        request,
        "reservations/reservation_confirmation.html",
        {
            "reservation": reservation,
        },
    )

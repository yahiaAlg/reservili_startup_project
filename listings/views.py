from django.conf import settings
from django.urls import reverse

from django.http import JsonResponse

# Create your views here
from .models import *


from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Restaurant, CarRentalAgency

# aggregate function for min max
from django.db.models.functions import Concat, Cast
from django.db.models import Min, Max, Avg, Value, F, CharField
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


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    print(f"Hotel Detail View: {hotel.slug}")
    context = {"object": hotel, "model_name": "Hotel"}
    return render(request, "listings/hotel_detail.html", context)


def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)

    # Define category mapping
    category_mapping = {
        "main": "main",
        "appetizers": "appetizer",
        "desserts": "dessert",
        "beverages": "beverage",
    }

    # Initialize menu_items dictionary
    menu_items = {}

    # Fetch and organize items by category
    for display_name, model_name in category_mapping.items():
        menu_items[display_name] = restaurant.menu_items.filter(
            category=model_name, is_available=True
        ).select_related("restaurant")

    context = {
        "object": restaurant,
        "model_name": "Restaurant",
        "menu_items": menu_items,
    }
    return render(request, "listings/restaurant_detail.html", context)


def car_rental_agency_detail(request, slug):
    agency = get_object_or_404(CarRentalAgency, slug=slug)
    context = {"object": agency, "model_name": "CarRentalAgency"}
    return render(request, "listings/car_rental_agency_detail.html", context)


def hotel_list(request):
    data_url = reverse("hotel_list_api")
    hotels = list(Hotel.objects.values("address"))

    max_price = Hotel.objects.aggregate(Max("price_per_night"))
    min_price = Hotel.objects.aggregate(Min("price_per_night"))

    max_price, min_price = max_price.get("price_per_night__max"), min_price.get(
        "price_per_night__min"
    )
    locations = [location.get("address", "no location") for location in hotels]
    print(locations)
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل الفنادق",
            "data_url": data_url,
            "min_price": min_price,
            "max_price": max_price,
            "price_step": (max_price - min_price) // 10,
            "locations": locations,
        },
    )


def restaurant_list(request):
    data_url = reverse("restaurant_list_api")
    restaurants = list(Restaurant.objects.values("address"))
    max_price = Restaurant.objects.aggregate(Max("price_range"))
    min_price = Restaurant.objects.aggregate(Min("price_range"))
    max_price, min_price = max_price.get("price_range__max"), min_price.get(
        "price_range__min"
    )
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل المطاعم",
            "data_url": data_url,
            "min_price": min_price,
            "max_price": max_price,
            "price_step": (max_price - min_price) // 10,
            "locations": [
                location.get("address", "no location") for location in restaurants
            ],
        },
    )


def car_rental_agency_list(request):
    data_url = reverse("car_rental_agency_list_api")
    agencies = list(CarRentalAgency.objects.values("address"))
    # extracting the list of max price_per_day for each agency the getting the max out of them

    max_price = Car.objects.aggregate(Max("price_per_day"))
    min_price = Car.objects.aggregate(Min("price_per_day"))

    max_price, min_price = max_price.get("price_per_day__max"), min_price.get(
        "price_per_day__min"
    )
    print(min_price)
    print(max_price)
    return render(
        request,
        "listings/listings.html",
        {
            "title": "كل وكالات كراء السيارات",
            "data_url": data_url,
            "min_price": min_price,
            "max_price": max_price,
            "price_step": (max_price - min_price) // 10,
            "locations": [
                location.get("address", "no location") for location in agencies
            ],
        },
    )


def hotel_list_api(request):
    hotels = list(
        Hotel.objects.annotate(
            image_url=Concat(
                Value(settings.MEDIA_URL),
                Cast("main_image", output_field=CharField()),
                output_field=CharField(),
            )
        ).values(
            "id", "name", "address", "price_per_night", "rating", "image_url", "slug"
        )
    )
    return JsonResponse(hotels, safe=False)


def restaurant_list_api(request):
    restaurants = list(
        Restaurant.objects.annotate(
            image_url=Concat(
                Value(settings.MEDIA_URL),
                Cast("main_image", output_field=CharField()),
                output_field=CharField(),
            )
        ).values("id", "name", "address", "price_range", "rating", "image_url", "slug")
    )
    return JsonResponse(restaurants, safe=False)


def car_rental_agency_list_api(request):
    # adding another column which is the average price of the price per day of the cars of the agency and making the image url a field for the src

    agencies = list(
        CarRentalAgency.objects.annotate(
            price_per_day=Avg("cars__price_per_day"),
            image_url=Concat(
                Value(settings.MEDIA_URL),
                Cast("main_image", output_field=CharField()),
                output_field=CharField(),
            ),
        ).values(
            "id",
            "name",
            "address",
            "rating",
            "image_url",
            "price_per_day",
            "slug",
        )
    )

    return JsonResponse(agencies, safe=False)


from .forms import get_reservation_form


def make_reservation(request, listing_type, slug):
    # Map listing types to their standardized versions
    listing_type_map = {
        "CarRentalAgency": "car-rental-agencies",
        "Hotel": "hotels",
        "Restaurant": "restaurants",
    }
    listing_type = listing_type_map.get(listing_type, "hotels")

    # Get the appropriate model and listing
    if listing_type == "hotels":
        listing = get_object_or_404(Hotel, slug=slug)
        kwargs = {"hotel": listing}
    elif listing_type == "restaurants":
        listing = get_object_or_404(Restaurant, slug=slug)
        kwargs = {"restaurant": listing}
    elif listing_type == "car-rental-agencies":
        listing = get_object_or_404(CarRentalAgency, slug=slug)
        kwargs = {"agency": listing}
    else:
        raise ValueError("Invalid listing type")

    if request.method == "POST":
        form = get_reservation_form(listing_type, data=request.POST, **kwargs)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user

            # Calculate total price based on listing type
            if listing_type == "hotels":
                reservation.hotel = listing
                # Calculate total nights
                nights = (reservation.check_out - reservation.check_in).days
                # Sum prices of all selected rooms
                room_prices = sum(
                    room.price_per_night for room in form.cleaned_data["rooms"]
                )
                reservation.total_price = room_prices * nights

            elif listing_type == "restaurants":
                reservation.restaurant = listing
                # Sum prices of all selected menu items
                reservation.total_price = sum(
                    item.price for item in form.cleaned_data["menu_items"]
                )

            elif listing_type == "car-rental-agencies":
                reservation.agency = listing
                # Calculate total days
                days = (reservation.end_date - reservation.start_date).days

                # Initialize total price
                total_price = 0

                # Calculate price for each car
                for car in form.cleaned_data["cars"]:
                    car_price = car.price_per_day

                    # Add driver cost if requested and car supports it
                    if reservation.with_driver and car.with_driver:
                        car_price += car.driver_cost_per_day

                    total_price += car_price * days

                # Adjust price based on insurance type
                if reservation.insurance_type == "full":
                    total_price *= 1.2  # 20% increase for full coverage

                reservation.total_price = total_price
            reservation.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect(
                "reservations/reservation_confirmation.html", reservation.id
            )
    else:
        form = get_reservation_form(listing_type, **kwargs)

    return render(
        request,
        "reservations/reservation.html",
        {
            "form": form,
            "listing_type": listing_type,
            "object": listing,
        },
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

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse

from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# import login required decorator
from django.contrib.auth.decorators import login_required

# import messages
from django.contrib import messages

# aggregate function for min max
from django.db.models.functions import Concat, Cast
from django.db.models import Min, Max, Avg, Value, CharField
import json
from decimal import Decimal

@login_required
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


@login_required
def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    # Get the content type for the Hotel model
    ct = ContentType.objects.get_for_model(Hotel)
    # Check if the hotel is in the current user's favorites
    is_favorited = request.user.favorites.filter(
        content_type=ct, object_id=hotel.id
    ).exists()
    context = {"object": hotel, "model_name": "Hotel", "is_favorited": is_favorited}
    return render(request, "listings/hotel_detail.html", context)


@login_required
def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)

    # Define category mapping and build menu_items dictionary (existing code)
    category_mapping = {
        "main": "main",
        "appetizers": "appetizer",
        "desserts": "dessert",
        "beverages": "beverage",
    }
    menu_items = {}
    for display_name, model_name in category_mapping.items():
        menu_items[display_name] = restaurant.menu_items.filter(
            category=model_name, is_available=True
        ).select_related("restaurant")

    # Get the content type for the Restaurant model
    ct = ContentType.objects.get_for_model(Restaurant)
    # Check if the restaurant is in the user's favourites
    is_favorited = request.user.favorites.filter(
        content_type=ct, object_id=restaurant.id
    ).exists()

    context = {
        "object": restaurant,
        "model_name": "Restaurant",
        "menu_items": menu_items,
        "is_favorited": is_favorited,
    }
    return render(request, "listings/restaurant_detail.html", context)


@login_required
def car_rental_agency_detail(request, slug):
    agency = get_object_or_404(CarRentalAgency, slug=slug)

    # Get the content type for the CarRentalAgency model
    ct = ContentType.objects.get_for_model(CarRentalAgency)
    # Check if the agency is in the user's favourites
    is_favorited = request.user.favorites.filter(
        content_type=ct, object_id=agency.id
    ).exists()

    context = {
        "object": agency,
        "model_name": "CarRentalAgency",
        "is_favorited": is_favorited,
    }
    return render(request, "listings/car_rental_agency_detail.html", context)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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
        reservation_type = "hotel"
    elif listing_type == "restaurants":
        listing = get_object_or_404(Restaurant, slug=slug)
        kwargs = {"restaurant": listing}
        reservation_type = "restaurant"
    elif listing_type == "car-rental-agencies":
        listing = get_object_or_404(CarRentalAgency, slug=slug)
        kwargs = {"agency": listing}
        reservation_type = "car"
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
                nights = (reservation.check_out - reservation.check_in).days
                room_prices = sum(
                    room.price_per_night for room in form.cleaned_data["rooms"]
                )
                reservation.total_price = room_prices * nights

            elif listing_type == "restaurants":
                reservation.restaurant = listing
                reservation.total_price = sum(
                    item.price for item in form.cleaned_data["menu_items"]
                )

            elif listing_type == "car-rental-agencies":
                reservation.agency = listing
                days = (reservation.end_date - reservation.start_date).days
                total_price = 0

                for car in form.cleaned_data["cars"]:
                    car_price = car.price_per_day
                    if reservation.with_driver and car.with_driver:
                        car_price += car.driver_cost_per_day
                    elif reservation.with_driver and not car.with_driver:
                        # If the user wants a driver but the car doesn't have one, add an notifiaction message to the user to inform him that this car is for rental only
                        messages.error(
                            request,
                            f"Car {car.name} is for rental only, you can't add a driver to it.",
                            )

                    total_price += car_price * days

                if reservation.insurance_type == "full":
                    total_price *= Decimal(1.2)

                reservation.total_price = total_price

            reservation.save()
            form.save_m2m()  # Save many-to-many relationships

            # Redirect to confirmation page with reservation type
            return redirect(
                "payment",
                listing_type=listing_type,
                reservation_id=reservation.id,
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


@login_required
def reservation_confirmation(request, reservation_type, reservation_id):
    # Map reservation types to models
    model_map = {
        "hotel": (HotelReservation, "hotel", "reservationroom_set"),
        "restaurant": (RestaurantReservation, "restaurant", "reservationmenuitem_set"),
        "car": (CarReservation, "agency", "reservationcar_set"),
    }

    # Get the appropriate model and related field
    Model, related_field, through_field = model_map.get(
        reservation_type, (None, None, None)
    )
    if not Model:
        messages.error(request, "Invalid reservation type")
        return redirect("index")

    # Get the reservation with related data
    reservation = get_object_or_404(
        Model.objects.select_related(related_field, "user").prefetch_related(
            f"{through_field}__{'room' if reservation_type == 'hotel' else 'menu_item' if reservation_type == 'restaurant' else 'car'}"
        ),
        id=reservation_id,
        user=request.user,
    )

    context = {"reservation": reservation, "reservation_type": reservation_type}
    return render(request, "reservations/reservation_confirmation.html", context)


# favorites/views.py
from django.contrib.contenttypes.models import ContentType
from pages.models import Favorite


@require_POST
@login_required
def toggle_favorite(request, listing_type, object_id):
    try:
        ct = ContentType.objects.get(model=listing_type)
    except ContentType.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Invalid listing type."}, status=400
        )

    # Try to get an existing favorite, or create one if not present.
    favorite, created = Favorite.objects.get_or_create(
        user=request.user, content_type=ct, object_id=object_id
    )
    if not created:
        # Already exists; remove it (toggle off)
        favorite.delete()
        favorited = False
    else:
        favorited = True

    return JsonResponse({"success": True, "favorited": favorited})

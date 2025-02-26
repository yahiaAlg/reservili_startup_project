# views.py
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotAllowed
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

from listings.models import *
from .models import *


@require_POST
@login_required
def mark_notification_read(request, notification_id):
    try:
        user_notification = UserNotification.objects.get(
            user=request.user, notification_id=notification_id
        )
    except UserNotification.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Notification not found"}, status=404
        )

    if not user_notification.is_read:
        user_notification.is_read = True
        user_notification.read_at = timezone.now()
        user_notification.save()

    unread_count = UserNotification.objects.filter(
        user=request.user, is_read=False
    ).count()
    return JsonResponse({"success": True, "unread_count": unread_count})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from listings.models import HotelReservation, RestaurantReservation, CarReservation


@login_required
def booking_view(request):
    # Get current datetime for comparison
    now = timezone.now()

    # Fetch all types of reservations for the current user
    hotel_reservations = (
        HotelReservation.objects.filter(user=request.user)
        .select_related("hotel")
        .prefetch_related("reservationroom_set__room")
    )
    restaurant_reservations = (
        RestaurantReservation.objects.filter(user=request.user)
        .select_related("restaurant")
        .prefetch_related("reservationmenuitem_set__menu_item")
    )
    car_reservations = (
        CarReservation.objects.filter(user=request.user)
        .select_related("agency")
        .prefetch_related("reservationcar_set__car")
    )

    # Prepare data structure for unified booking display
    bookings = []

    # Process hotel reservations
    for reservation in hotel_reservations:
        rooms = reservation.reservationroom_set.all()
        room_details = ", ".join(
            [
                f"{room.room.get_room_type_display()} {room.room.room_number}"
                for room in rooms
            ]
        )
        booking = {
            "type": "hotel",
            "booking_number": f"H{reservation.id:08d}",
            "date_str": f"{reservation.check_in.strftime('%d %B %Y')} - {reservation.check_out.strftime('%d %B %Y')}",
            "name": reservation.hotel.name,
            "rating": reservation.hotel.rating,
            "location": reservation.hotel.address,
            "image": (
                reservation.hotel.main_image.url
                if reservation.hotel.main_image
                else None
            ),
            "detail_url": reservation.hotel.get_absolute_url(),
            "is_upcoming": reservation.check_in > now.date(),
            "status": reservation.status,
            "reservation_id": reservation.id,
            "listing_type": "hotels",
            "details": room_details,
            "sort_date": reservation.check_in,  # used for sorting
        }
        bookings.append(booking)

    # Process restaurant reservations
    for reservation in restaurant_reservations:
        menu_items = reservation.reservationmenuitem_set.all()
        menu_item_details = ", ".join([f"{item.menu_item.name}" for item in menu_items])
        booking = {
            "type": "restaurant",
            "booking_number": f"R{reservation.id:08d}",
            "date_str": f"{reservation.reservation_date.strftime('%d %B %Y')}, {reservation.reservation_time.strftime('%I:%M %p')}",
            "name": reservation.restaurant.name,
            "rating": reservation.restaurant.rating,
            "location": reservation.restaurant.address,
            "image": (
                reservation.restaurant.main_image.url
                if reservation.restaurant.main_image
                else None
            ),
            "detail_url": reservation.restaurant.get_absolute_url(),
            "is_upcoming": (reservation.reservation_date > now.date())
            or (
                reservation.reservation_date == now.date()
                and reservation.reservation_time > now.time()
            ),
            "status": reservation.status,
            "reservation_id": reservation.id,
            "listing_type": "restaurants",
            "details": menu_item_details,
            "sort_date": reservation.reservation_date,  # used for sorting
        }
        bookings.append(booking)

    # Process car reservations
    for reservation in car_reservations:
        cars = reservation.reservationcar_set.all()
        car_details = ", ".join([f"{car.car.brand} {car.car.model}" for car in cars])
        booking = {
            "type": "car",
            "booking_number": f"C{reservation.id:08d}",
            "date_str": f"{reservation.start_date.strftime('%d %B %Y')} - {reservation.end_date.strftime('%d %B %Y')}",
            "name": reservation.agency.name,
            "rating": reservation.agency.rating,
            "location": reservation.agency.address,
            "image": (
                reservation.agency.main_image.url
                if reservation.agency.main_image
                else None
            ),
            "detail_url": reservation.agency.get_absolute_url(),
            "is_upcoming": reservation.start_date > now.date(),
            "status": reservation.status,
            "reservation_id": reservation.id,
            "listing_type": "car-rental-agencies",
            "details": car_details,
            "sort_date": reservation.start_date,  # used for sorting
        }
        bookings.append(booking)

    # Check for query parameter to determine sort order.
    # Assume order=upcoming means sort ascending (earlier dates first)
    # and order=past means sort descending.
    order = request.GET.get("order", "past")
    if order == "upcoming":
        bookings.sort(key=lambda x: x["sort_date"], reverse=False)
    else:
        bookings.sort(key=lambda x: x["sort_date"], reverse=True)

    context = {
        "bookings": bookings,
        "order": order,
    }
    return render(request, "pages/booking.html", context)


# A mapping from URL listing type to the actual reservation model
RESERVATION_MODELS = {
    "hotel": HotelReservation,
    "restaurant": RestaurantReservation,
    "car": CarReservation,
}


@login_required
def cancel_reservation(request, listing_type, reservation_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Determine which reservation model to use based on the listing_type
    model = RESERVATION_MODELS.get(listing_type)
    if not model:
        messages.error(request, "Invalid reservation type.")
        return redirect("booking")  # Replace 'booking' with your appropriate URL name

    # Retrieve the reservation and ensure it belongs to the logged-in user
    reservation = get_object_or_404(model, id=reservation_id, user=request.user)

    # Ensure it hasn't been cancelled already
    if reservation.status == "cancelled":
        messages.error(request, "Reservation is already cancelled.")
        return redirect("booking")

    # Set the status to 'cancelled' and save the reservation
    reservation.status = "cancelled"
    # delete the reservation from the database
    reservation.delete()
    messages.success(request, "Reservation cancelled successfully.")
    return redirect("booking")


@login_required
def bookmark_view(request):
    # Get ContentType objects for each listing type.
    hotel_ct = ContentType.objects.get(model="hotel")
    restaurant_ct = ContentType.objects.get(model="restaurant")
    carrental_ct = ContentType.objects.get(model="carrentalagency")

    # Retrieve user favourites filtered by listing type.
    hotel_favorites = Favorite.objects.filter(user=request.user, content_type=hotel_ct)
    restaurant_favorites = Favorite.objects.filter(
        user=request.user, content_type=restaurant_ct
    )
    carrental_favorites = Favorite.objects.filter(
        user=request.user, content_type=carrental_ct
    )

    context = {
        "hotel_favorites": hotel_favorites,
        "restaurant_favorites": restaurant_favorites,
        "carrental_favorites": carrental_favorites,
    }
    return render(request, "pages/bookmark.html", context)


# search views
import math
from django.db.models import Q, Min, Max, Avg
from listings.models import *


def agency_search(request):
    # Get search parameters from GET query string, with defaults
    city = request.GET.get("city", "الجزائر")
    selected_brand = request.GET.get("brand", "")
    selected_model = request.GET.get("model", "")
    selected_price_range = request.GET.get("price_range", "")

    # Service switches; if checked, value will be "1"
    service_24hr = request.GET.get("service_24hr", "")
    driver_service = request.GET.get("driver_service", "")
    airport_pickup = request.GET.get("airport_pickup", "")
    long_term = request.GET.get("long_term", "")
    short_term = request.GET.get("short_term", "")
    full_insurance = request.GET.get("full_insurance", "")

    # Filter agencies by city using Q() to match against address or name
    agencies = CarRentalAgency.objects.filter(
        Q(address__icontains=city) | Q(name__icontains=city)
    )

    # Filter by brand if provided
    if selected_brand:
        agencies = agencies.filter(cars__brand=selected_brand)

    # Filter by model if provided
    if selected_model:
        agencies = agencies.filter(cars__model=selected_model)

    # Filter by price range (applied against related Car prices)
    if selected_price_range:
        try:
            start, end = map(lambda x: int(x.strip()), selected_price_range.split("-"))
            agencies = agencies.filter(
                cars__price_per_day__gte=start, cars__price_per_day__lte=end
            ).distinct()
        except ValueError:
            pass

    # Filter by service availability using the provided switches
    if service_24hr == "1":
        agencies = agencies.filter(has_24hr_service=True)
    if driver_service == "1":
        agencies = agencies.filter(has_driver_service=True)
    if airport_pickup == "1":
        agencies = agencies.filter(has_airport_pickup=True)
    if long_term == "1":
        agencies = agencies.filter(has_long_term_rental=True)
    if short_term == "1":
        agencies = agencies.filter(has_short_term_rental=True)
    if full_insurance == "1":
        agencies = agencies.filter(has_full_insurance=True)

    # Compute dynamic price options based on Car prices
    price_data = Car.objects.aggregate(
        min_price=Min("price_per_day"), max_price=Max("price_per_day")
    )
    min_price = price_data["min_price"]
    max_price = price_data["max_price"]

    price_options = []
    if min_price is not None and max_price is not None:
        num_options = 4
        step = math.ceil((max_price - min_price) / num_options)
        start_value = min_price
        for i in range(num_options):
            end_value = start_value + step
            price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    # Get distinct brand and model options from the Car model
    brand_options = Car.objects.values_list("brand", flat=True).distinct()
    model_options = Car.objects.values_list("model", flat=True).distinct()

    context = {
        "agencies": agencies,
        "city": city,
        "selected_brand": selected_brand,
        "selected_model": selected_model,
        "brand_options": brand_options,
        "model_options": model_options,
        "price_options": price_options,
        "selected_price_range": selected_price_range,
        # Pass the service switch values for pre-selection
        "service_24hr": service_24hr,
        "driver_service": driver_service,
        "airport_pickup": airport_pickup,
        "long_term": long_term,
        "short_term": short_term,
        "full_insurance": full_insurance,
    }
    return render(request, "pages/agency_search.html", context)


def hotel_search(request):
    # Get search parameters from GET query string with defaults
    city = request.GET.get("city", "الجزائر")
    selected_room_type = request.GET.get("room_type", "")
    selected_capacity = request.GET.get("capacity", "")
    selected_price_range = request.GET.get("price_range", "")

    # Amenity switches (if checked, value will be "1")
    wifi = request.GET.get("wifi", "")
    parking = request.GET.get("parking", "")
    swimming_pool = request.GET.get("swimming_pool", "")
    fitness_center = request.GET.get("fitness_center", "")
    restaurant_amenity = request.GET.get("restaurant", "")
    reception = request.GET.get("reception", "")
    non_smoking_rooms = request.GET.get("non_smoking_rooms", "")

    # Filter hotels by city (searching in address or name)
    hotels = Hotel.objects.filter(Q(address__icontains=city) | Q(name__icontains=city))

    # Annotate hotels with the average room price per night from related rooms
    hotels = hotels.annotate(avg_room_price=Avg("rooms__price_per_night"))

    # Filter by room type if provided
    if selected_room_type:
        hotels = hotels.filter(rooms__room_type=selected_room_type)

    # Filter by capacity if provided
    if selected_capacity:
        try:
            cap = int(selected_capacity)
            hotels = hotels.filter(rooms__capacity=cap)
        except ValueError:
            pass

    # Filter by amenities based on the switches
    if wifi == "1":
        hotels = hotels.filter(has_wifi=True)
    if parking == "1":
        hotels = hotels.filter(has_parking=True)
    if swimming_pool == "1":
        hotels = hotels.filter(has_swimming_pool=True)
    if fitness_center == "1":
        hotels = hotels.filter(
            has_gym=True
        )  # assuming has_gym represents Fitness Center
    if restaurant_amenity == "1":
        hotels = hotels.filter(has_restaurant=True)
    if reception == "1":
        hotels = hotels.filter(has_24hr_reception=True)
    if non_smoking_rooms == "1":
        hotels = hotels.filter(has_non_smoking_rooms=True)

    # Optionally filter by average room price if a price range is provided.
    if selected_price_range:
        try:
            start, end = map(lambda x: int(x.strip()), selected_price_range.split("-"))
            hotels = hotels.filter(avg_room_price__gte=start, avg_room_price__lte=end)
        except ValueError:
            pass

    # Compute dynamic price options based on Room prices for filtered hotels
    price_data = Room.objects.filter(hotel__in=hotels).aggregate(
        min_price=Min("price_per_night"), max_price=Max("price_per_night")
    )
    min_price = price_data["min_price"]
    max_price = price_data["max_price"]

    price_options = []
    if min_price is not None and max_price is not None and (max_price - min_price) > 0:
        num_options = 4
        step = math.ceil((max_price - min_price) / num_options)
        start_value = min_price
        for i in range(num_options):
            end_value = start_value + step
            price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    # Get distinct room type and capacity options from the Room model
    room_type_options = Room.objects.values_list("room_type", flat=True).distinct()
    capacity_options = (
        Room.objects.values_list("capacity", flat=True).distinct().order_by("capacity")
    )

    context = {
        "hotels": hotels,
        "city": city,
        "selected_room_type": selected_room_type,
        "selected_capacity": selected_capacity,
        "selected_price_range": selected_price_range,
        "price_options": price_options,
        "room_type_options": room_type_options,
        "capacity_options": capacity_options,
        # Pass amenity switch values for pre-selection in the template
        "wifi": wifi,
        "parking": parking,
        "swimming_pool": swimming_pool,
        "fitness_center": fitness_center,
        "restaurant": restaurant_amenity,
        "reception": reception,
        "non_smoking_rooms": non_smoking_rooms,
    }
    return render(request, "pages/hotel_search.html", context)


def restaurant_search(request):
    # Get search parameters (with defaults)
    city = request.GET.get("city", "الجزائر")
    hot = request.GET.get("hot", "")
    cold = request.GET.get("cold", "")
    beverage = request.GET.get("beverage", "")
    dessert = request.GET.get("dessert", "")
    salad = request.GET.get("salad", "")
    table_type = request.GET.get("table_type", "")
    menu_category = request.GET.get("menu_category", "")
    selected_price_range = request.GET.get("price_range", "")

    # Base filtering: match restaurants by city (in address or name)
    restaurants = Restaurant.objects.filter(
        Q(address__icontains=city) | Q(name__icontains=city)
    )

    # Build a Q object for the menu category switches
    filters = Q()
    if hot == "1":
        filters &= Q(has_hot_dishes=True)
    if cold == "1":
        filters &= Q(has_cold_dishes=True)
    if beverage == "1":
        filters &= Q(has_beverages=True)
    if dessert == "1":
        filters &= Q(has_desserts=True)
    if salad == "1":
        filters &= Q(has_salads=True)
    if filters:
        restaurants = restaurants.filter(filters)

    # Filter by table type if provided
    if table_type:
        if table_type == "Family Tables":
            restaurants = restaurants.filter(has_family_tables=True)
        elif table_type == "Business Tables":
            restaurants = restaurants.filter(has_business_tables=True)
        elif table_type == "Private Tables":
            restaurants = restaurants.filter(has_private_tables=True)

    # Filter by menu items category if provided (restaurants having at least one such item)
    if menu_category:
        restaurants = restaurants.filter(menu_items__category=menu_category)

    # Annotate each restaurant with the average price from its menu items
    restaurants = restaurants.annotate(avg_price=Avg("menu_items__price"))

    # Filter by average price range if provided
    if selected_price_range:
        try:
            start, end = map(lambda x: int(x.strip()), selected_price_range.split("-"))
            restaurants = restaurants.filter(avg_price__gte=start, avg_price__lte=end)
        except ValueError:
            pass

    # Compute dynamic price options based on MenuItem prices for the filtered restaurants
    price_data = MenuItem.objects.filter(restaurant__in=restaurants).aggregate(
        min_price=Min("price"), max_price=Max("price")
    )
    min_price = price_data["min_price"]
    max_price = price_data["max_price"]

    price_options = []
    if min_price is not None and max_price is not None and (max_price - min_price) > 0:
        num_options = 4
        step = math.ceil((max_price - min_price) / num_options)
        start_value = min_price
        for i in range(num_options):
            end_value = start_value + step
            price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    # Get distinct menu category options for the select field
    menu_category_options = (
        MenuItem.objects.filter(restaurant__in=restaurants)
        .values_list("category", flat=True)
        .distinct()
    )

    context = {
        "restaurants": restaurants,
        "city": city,
        "hot": hot,
        "cold": cold,
        "beverage": beverage,
        "dessert": dessert,
        "salad": salad,
        "table_type": table_type,
        "menu_category": menu_category,
        "selected_price_range": selected_price_range,
        "price_options": price_options,
        "menu_category_options": menu_category_options,
    }
    return render(request, "pages/restaurant_search.html", context)


import random
import math
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from listings.models import Hotel, Restaurant, CarRentalAgency, Room, MenuItem, Car


@login_required
def index_view(request):
    # Recent sections
    carousel_slides = CarouselSlide.objects.filter(is_active=True).order_by("order")
    hotels = list(Hotel.objects.all())
    random.shuffle(hotels)
    recent_hotels = hotels[:4]

    restaurants = list(Restaurant.objects.all())
    random.shuffle(restaurants)
    recent_restaurants = restaurants[:4]

    car_agencies = list(CarRentalAgency.objects.all())
    random.shuffle(car_agencies)
    recent_car_agencies = car_agencies[:4]

    # --- For Hotel Search Form ---
    # Room type and capacity options (for hotels)
    room_type_options = Room.objects.values_list("room_type", flat=True).distinct()
    capacity_options = (
        Room.objects.values_list("capacity", flat=True).distinct().order_by("capacity")
    )
    # Dynamic price options based on Room.price_per_night
    price_data_hotel = Room.objects.aggregate(
        min_price=Min("price_per_night"), max_price=Min("price_per_night")
    )
    # (It might be better to use Max instead of Min for max_price)
    price_data_hotel = Room.objects.aggregate(
        min_price=Min("price_per_night"), max_price=Max("price_per_night")
    )
    min_price_hotel = price_data_hotel["min_price"]
    max_price_hotel = price_data_hotel["max_price"]
    hotel_price_options = []
    if (
        min_price_hotel is not None
        and max_price_hotel is not None
        and (max_price_hotel - min_price_hotel) > 0
    ):
        num_options = 4
        step = math.ceil((max_price_hotel - min_price_hotel) / num_options)
        start_value = min_price_hotel
        for i in range(num_options):
            end_value = start_value + step
            hotel_price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    # --- For Restaurant Search Form ---
    # Distinct menu categories from MenuItem
    menu_category_options = MenuItem.objects.values_list(
        "category", flat=True
    ).distinct()
    # Dynamic price options based on MenuItem.price
    price_data_restaurant = MenuItem.objects.aggregate(
        min_price=Min("price"), max_price=Max("price")
    )
    min_price_restaurant = price_data_restaurant["min_price"]
    max_price_restaurant = price_data_restaurant["max_price"]
    restaurant_price_options = []
    if (
        min_price_restaurant is not None
        and max_price_restaurant is not None
        and (max_price_restaurant - min_price_restaurant) > 0
    ):
        num_options = 4
        step = math.ceil((max_price_restaurant - min_price_restaurant) / num_options)
        start_value = min_price_restaurant
        for i in range(num_options):
            end_value = start_value + step
            restaurant_price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    # --- For Car Search Form ---
    brand_options = Car.objects.values_list("brand", flat=True).distinct()
    model_options = Car.objects.values_list("model", flat=True).distinct()
    price_data_car = Car.objects.aggregate(
        min_price=Min("price_per_day"), max_price=Max("price_per_day")
    )
    min_price_car = price_data_car["min_price"]
    max_price_car = price_data_car["max_price"]
    car_price_options = []
    if (
        min_price_car is not None
        and max_price_car is not None
        and (max_price_car - min_price_car) > 0
    ):
        num_options = 4
        step = math.ceil((max_price_car - min_price_car) / num_options)
        start_value = min_price_car
        for i in range(num_options):
            end_value = start_value + step
            car_price_options.append(f"{start_value} - {end_value}")
            start_value = end_value + 1

    context = {
        "recent_hotels": recent_hotels,
        "recent_restaurants": recent_restaurants,
        "recent_car_agencies": recent_car_agencies,
        # For hotel search form
        "room_type_options": room_type_options,
        "capacity_options": capacity_options,
        "hotel_price_options": hotel_price_options,
        # For restaurant search form
        "menu_category_options": menu_category_options,
        "restaurant_price_options": restaurant_price_options,
        # For car search form
        "brand_options": brand_options,
        "model_options": model_options,
        "car_price_options": car_price_options,
        "carousel_slides": carousel_slides,
    }

    return render(request, "pages/index.html", context)

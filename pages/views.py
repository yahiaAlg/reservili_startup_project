from django.shortcuts import render
from listings.models import *
import random


def index_view(request):
    # Shuffle and get the first four objects for each model
    hotels = list(Hotel.objects.all())
    random.shuffle(hotels)
    recent_hotels = hotels[:4]

    restaurants = list(Restaurant.objects.all())
    random.shuffle(restaurants)
    recent_restaurants = restaurants[:4]

    car_agencies = list(CarRentalAgency.objects.all())
    random.shuffle(car_agencies)
    recent_car_agencies = car_agencies[:4]

    context = {
        "recent_hotels": recent_hotels,
        "recent_restaurants": recent_restaurants,
        "recent_car_agencies": recent_car_agencies,
    }

    return render(request, "pages/index.html", context)


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from listings.models import (
    HotelReservation,
    RestaurantReservation,
    CarReservation,
)


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
                f"{room.quantity} x {room.room.get_room_type_display()} {room.room.room_number}"
                for room in rooms
            ]
        )

        booking = {
            "type": "hotel",
            "booking_number": f"H{reservation.id:08d}",
            "date_str": f"{reservation.check_in.strftime('%d %B %Y')} - {reservation.check_out.strftime('%d %B %Y')}",
            "name": reservation.hotel.name,
            "rating": reservation.hotel.rating,
            "reviews_count": reservation.hotel.reviews.count(),
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
        }
        bookings.append(booking)

    # Process restaurant reservations
    for reservation in restaurant_reservations:
        menu_items = reservation.reservationmenuitem_set.all()
        menu_item_details = ", ".join(
            [f"{item.quantity} x {item.menu_item.name}" for item in menu_items]
        )

        booking = {
            "type": "restaurant",
            "booking_number": f"R{reservation.id:08d}",
            "date_str": f"{reservation.reservation_date.strftime('%d %B %Y')}, {reservation.reservation_time.strftime('%I:%M %p')}",
            "name": reservation.restaurant.name,
            "rating": reservation.restaurant.rating,
            "reviews_count": reservation.restaurant.reviews.count(),
            "location": reservation.restaurant.address,
            "image": (
                reservation.restaurant.main_image.url
                if reservation.restaurant.main_image
                else None
            ),
            "detail_url": reservation.restaurant.get_absolute_url(),
            "is_upcoming": reservation.reservation_date > now.date()
            or (
                reservation.reservation_date == now.date()
                and reservation.reservation_time > now.time()
            ),
            "status": reservation.status,
            "reservation_id": reservation.id,
            "listing_type": "restaurants",
            "details": menu_item_details,
        }
        bookings.append(booking)

    # Process car reservations
    for reservation in car_reservations:
        cars = reservation.reservationcar_set.all()
        car_details = ", ".join(
            [f"{car.quantity} x {car.car.brand} {car.car.model}" for car in cars]
        )

        booking = {
            "type": "car",
            "booking_number": f"C{reservation.id:08d}",
            "date_str": f"{reservation.start_date.strftime('%d %B %Y')} - {reservation.end_date.strftime('%d %B %Y')}",
            "name": f"{reservation.agency.name}",
            "rating": reservation.agency.rating,
            "reviews_count": reservation.agency.reviews.count(),
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
        }
        bookings.append(booking)

    # Sort bookings by date
    bookings.sort(key=lambda x: x["booking_number"], reverse=True)

    context = {
        "bookings": bookings,
    }

    return render(request, "reservations/my_bookings.html", context)


def bookmark_view(request):
    return render(request, "pages/bookmark.html")

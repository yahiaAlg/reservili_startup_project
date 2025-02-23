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


@login_required
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
        car_details = ", ".join([f"{car.car.brand} {car.car.model}" for car in cars])

        booking = {
            "type": "car",
            "booking_number": f"C{reservation.id:08d}",
            "date_str": f"{reservation.start_date.strftime('%d %B %Y')} - {reservation.end_date.strftime('%d %B %Y')}",
            "name": f"{reservation.agency.name}",
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
        }
        bookings.append(booking)

    # Sort bookings by date
    bookings.sort(key=lambda x: x["booking_number"], reverse=True)

    context = {
        "bookings": bookings,
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

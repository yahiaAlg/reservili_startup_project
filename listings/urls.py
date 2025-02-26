from django.urls import path
from . import views

urlpatterns = [
    path("hotels/<slug:slug>/", views.hotel_detail, name="hotel_detail"),
    path("restaurants/<slug:slug>/", views.restaurant_detail, name="restaurant_detail"),
    path(
        "car-rental-agencies/<slug:slug>/",
        views.car_rental_agency_detail,
        name="car_rental_agency_detail",
    ),
    path(
        "api/<str:listing_type>/<slug:slug>/rate/",
        views.update_rating,
        name="update_rating",
    ),
    path("hotels/", views.hotel_list, name="hotel_list"),
    path("restaurants/", views.restaurant_list, name="restaurant_list"),
    path(
        "car-rental-agencies/",
        views.car_rental_agency_list,
        name="car_rental_agency_list",
    ),
    path("api/hotels/", views.hotel_list_api, name="hotel_list_api"),
    path("api/restaurants/", views.restaurant_list_api, name="restaurant_list_api"),
    path(
        "api/car-rental-agencies/",
        views.car_rental_agency_list_api,
        name="car_rental_agency_list_api",
    ),
    # reservation
    path(
        "reservations/<str:listing_type>/<slug:slug>",
        views.make_reservation,
        name="reservation",
    ),
    path(
        "reservation-confirmation/<str:reservation_type>/<int:reservation_id>/",
        views.reservation_confirmation,
        name="reservation_confirmation",
    ),
    path(
        "toggle/<str:listing_type>/<int:object_id>/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
]

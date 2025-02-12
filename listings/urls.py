from django.urls import path
from . import views

urlpatterns = [
    path("hotels/<slug:slug>/", views.HotelDetailView.as_view(), name="hotel_detail"),
    path(
        "restaurants/<slug:slug>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
    path(
        "car-rental-agencies/<slug:slug>/",
        views.CarRentalAgencyDetailView.as_view(),
        name="car_rental_agency_detail",
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
]

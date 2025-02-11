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
    path("hotels/", views.HotelListView.as_view(), name="hotel_list"),
    path("restaurants/", views.RestaurantListView.as_view(), name="restaurant_list"),
    path(
        "car-rental-agencies/",
        views.CarRentalAgencyListView.as_view(),
        name="car_rental_agency_list",
    ),
]

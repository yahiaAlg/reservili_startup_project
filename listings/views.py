from django.shortcuts import render
from django.urls import reverse

from django.http import JsonResponse

# Create your views here
from django.views.generic import DetailView
from .models import *


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "listings/hotel_detail.html"


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "listings/restaurant_detail.html"


class CarRentalAgencyDetailView(DetailView):
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

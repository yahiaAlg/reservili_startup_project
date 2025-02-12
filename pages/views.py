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


def booking_view(request):
    return render(request, "pages/booking.html")


def bookmark_view(request):
    return render(request, "pages/bookmark.html")

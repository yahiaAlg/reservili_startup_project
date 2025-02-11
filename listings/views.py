from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView
from .models import *


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotel_detail.html"


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "restaurant_detail.html"


class CarRentalAgencyDetailView(DetailView):
    model = CarRentalAgency
    template_name = "car_rental_agency_detail.html"


class HotelListView(ListView):
    model = Hotel
    template_name = "hotel_list.html"
    context_object_name = "hotels"
    paginate_by = 10  # Number of items per page


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "restaurant_list.html"
    context_object_name = "restaurants"
    paginate_by = 10  # Number of items per page


class CarRentalAgencyListView(ListView):
    model = CarRentalAgency
    template_name = "car_rental_agency_list.html"
    context_object_name = "agencies"
    paginate_by = 10  # Number of items per page

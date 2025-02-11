# admin.py
from django.contrib import admin
from .models import *


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 3


class CarAgencyImageInline(admin.TabularInline):
    model = CarAgencyImage
    extra = 3


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "price_per_night", "has_wifi", "has_parking")
    list_filter = ("has_wifi", "has_parking", "has_swimming_pool", "has_gym")
    search_fields = ("name", "description", "address")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "address",
                    "description",
                    "rating",
                    "price_per_night",
                    "main_image",
                )
            },
        ),
        (
            "Amenities",
            {
                "fields": (
                    "has_wifi",
                    "has_parking",
                    "has_swimming_pool",
                    "has_gym",
                    "has_restaurant",
                    "has_24hr_reception",
                    "has_non_smoking_rooms",
                )
            },
        ),
    )
    inlines = [HotelImageInline]


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ("hotel", "caption")
    search_fields = ("hotel__name", "caption")


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "price_range")
    list_filter = ("has_family_tables", "has_business_tables", "has_private_tables")
    search_fields = ("name", "description", "address")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "address",
                    "description",
                    "rating",
                    "price_range",
                    "main_image",
                )
            },
        ),
        (
            "Table Types",
            {
                "fields": (
                    "has_family_tables",
                    "has_business_tables",
                    "has_private_tables",
                )
            },
        ),
        (
            "Menu Categories",
            {
                "fields": (
                    "has_hot_dishes",
                    "has_cold_dishes",
                    "has_beverages",
                    "has_desserts",
                    "has_salads",
                )
            },
        ),
    )

    inlines = [RestaurantImageInline]


class CarInline(admin.TabularInline):
    model = Car
    extra = 1


@admin.register(CarRentalAgency)
class CarRentalAgencyAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "has_24hr_service")
    list_filter = ("has_driver_service", "has_airport_pickup", "has_full_insurance")
    search_fields = ("name", "description", "address")
    inlines = [CarInline]
    fieldsets = (
        (None, {"fields": ("name", "address", "description", "rating", "main_image")}),
        (
            "Services",
            {
                "fields": (
                    "has_24hr_service",
                    "has_driver_service",
                    "has_airport_pickup",
                    "has_long_term_rental",
                    "has_short_term_rental",
                    "has_full_insurance",
                )
            },
        ),
    )
    inlines = [CarAgencyImageInline, CarInline]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "price_per_day", "is_available", "agency")
    list_filter = ("brand", "is_available", "transmission", "agency")
    search_fields = ("brand", "model")


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "caption")
    search_fields = ("restaurant__name", "caption")


@admin.register(CarAgencyImage)
class CarAgencyImageAdmin(admin.ModelAdmin):
    list_display = ("agency", "caption")
    search_fields = ("agency__name", "caption")

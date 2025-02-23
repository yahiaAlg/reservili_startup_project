# admin.py
from django.contrib import admin
from .models import *


# Inline Classes
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 3


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


class CarAgencyImageInline(admin.TabularInline):
    model = CarAgencyImage
    extra = 3


class CarInline(admin.TabularInline):
    model = Car
    extra = 1


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


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
    inlines = [HotelImageInline, RoomInline]


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

    inlines = [RestaurantImageInline, MenuItemInline]


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
    list_display = (
        "brand",
        "model",
        "year",
        "price_per_day",
        "driver_cost_per_day",
        "with_driver",
        "is_available",
        "agency",
    )
    list_filter = ("brand", "is_available", "transmission", "agency", "with_driver")
    search_fields = ("brand", "model")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "agency",
                    "brand",
                    "model",
                    "year",
                    "transmission",
                    "price_per_day",
                    "is_available",
                    "image",
                )
            },
        ),
        ("Driver Service", {"fields": ("with_driver", "driver_cost_per_day")}),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "hotel",
        "room_type",
        "room_number",
        "floor",
        "capacity",
        "price_per_night",
        "is_available",
    )
    list_filter = (
        "hotel",
        "room_type",
        "floor",
        "is_available",
        "has_air_conditioning",
        "has_sea_view",
    )
    search_fields = ("hotel__name", "room_number", "description")
    readonly_fields = ("id",)
    inlines = [RoomImageInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "hotel",
                    "room_type",
                    "room_number",
                    "floor",
                    "capacity",
                    "price_per_night",
                    "size_sqm",
                    "is_available",
                )
            },
        ),
        (
            "Amenities",
            {
                "fields": (
                    "has_air_conditioning",
                    "has_heating",
                    "has_minibar",
                    "has_tv",
                    "has_safe",
                    "has_private_bathroom",
                    "has_sea_view",
                    "has_balcony",
                )
            },
        ),
        ("Details", {"fields": ("description", "image")}),
    )


class MenuItemImageInline(admin.TabularInline):
    model = MenuItemImage
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "restaurant",
        "category",
        "price",
        "is_available",
        "is_vegetarian",
        "spiciness_level",
    )
    list_filter = (
        "restaurant",
        "category",
        "is_available",
        "is_vegetarian",
        "is_vegan",
        "is_gluten_free",
    )
    search_fields = ("name", "restaurant__name", "description")
    readonly_fields = ("id",)
    inlines = [MenuItemImageInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("restaurant", "name", "category", "price", "is_available")},
        ),
        (
            "Dietary Information",
            {
                "fields": (
                    "is_vegetarian",
                    "is_vegan",
                    "is_gluten_free",
                    "spiciness_level",
                    "calories",
                )
            },
        ),
        ("Preparation", {"fields": ("preparation_time",)}),
        ("Details", {"fields": ("description", "image")}),
    )


# Inline admin for ReservationRoom
class ReservationRoomInline(admin.TabularInline):
    model = ReservationRoom
    extra = 1
    autocomplete_fields = ["room"]


# Admin configuration for HotelReservation
@admin.register(HotelReservation)
class HotelReservationAdmin(admin.ModelAdmin):
    list_display = (
        "hotel",
        "user",
        "check_in",
        "check_out",
        "number_of_guests",
        "status",
        "total_price",
        "room_types",
    )
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("user__username", "hotel__name")
    date_hierarchy = "check_in"
    inlines = [ReservationRoomInline]

    def room_types(self, obj):
        return ", ".join([room.get_room_type_display() for room in obj.rooms.all()])

    room_types.short_description = "Room Types"


# Inline admin for ReservationCar
class ReservationCarInline(admin.TabularInline):
    model = ReservationCar
    extra = 1
    autocomplete_fields = ["car"]


# Admin configuration for CarReservation
@admin.register(CarReservation)
class CarReservationAdmin(admin.ModelAdmin):
    list_display = (
        "agency",
        "user",
        "start_date",
        "end_date",
        "status",
        "total_price",
        "car_brands",
    )
    list_filter = ("status", "start_date", "end_date", "with_driver")
    search_fields = ("user__username", "agency__name")
    date_hierarchy = "start_date"
    inlines = [ReservationCarInline]

    def car_brands(self, obj):
        return ", ".join([car.brand for car in obj.cars.all()])

    car_brands.short_description = "Car Brands"


# Inline admin for ReservationMenuItem
class ReservationMenuItemInline(admin.TabularInline):
    model = ReservationMenuItem
    extra = 1
    autocomplete_fields = ["menu_item"]


# Admin configuration for RestaurantReservation
@admin.register(RestaurantReservation)
class RestaurantReservationAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "user",
        "reservation_date",
        "reservation_time",
        "table_type",
        "status",
        "total_price",
        "menu_items",
    )
    list_filter = ("status", "reservation_date", "table_type")
    search_fields = ("user__username", "restaurant__name")
    date_hierarchy = "reservation_date"
    inlines = [ReservationMenuItemInline]

    def menu_items(self, obj):
        return ", ".join([item.name for item in obj.menu_items.all()])

    menu_items.short_description = "Menu Items"


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ("room", "caption")
    list_filter = ("room__hotel",)
    search_fields = ("room__hotel__name", "room__room_number", "caption")


@admin.register(MenuItemImage)
class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "caption")
    list_filter = ("menu_item__restaurant",)
    search_fields = ("menu_item__name", "menu_item__restaurant__name", "caption")


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "caption")
    search_fields = ("restaurant__name", "caption")


@admin.register(CarAgencyImage)
class CarAgencyImageAdmin(admin.ModelAdmin):
    list_display = ("agency", "caption")
    search_fields = ("agency__name", "caption")

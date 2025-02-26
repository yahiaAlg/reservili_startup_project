# Create your models here.
# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.urls import reverse


class Hotel(models.Model):
    name = models.CharField(_("Hotel Name"), max_length=255)
    slug = AutoSlugField(populate_from="name", default="", unique=True)
    address = models.CharField(_("Address"), max_length=500)
    description = models.TextField(_("Description"))
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=5)
    price_per_night = models.DecimalField(
        _("Price per Night"), max_digits=10, decimal_places=2
    )

    # Amenities
    has_wifi = models.BooleanField(_("WiFi"), default=False)
    has_parking = models.BooleanField(_("Private Parking"), default=False)
    has_swimming_pool = models.BooleanField(_("Swimming Pool"), default=False)
    has_gym = models.BooleanField(_("Fitness Center"), default=False)
    has_restaurant = models.BooleanField(_("Restaurant"), default=False)
    has_24hr_reception = models.BooleanField(_("24/7 Reception"), default=False)
    has_non_smoking_rooms = models.BooleanField(_("Non-smoking Rooms"), default=False)

    # Media
    main_image = models.ImageField(
        _("Main Image"),
        upload_to="hotels/main/",
        null=True,
        blank=True,
        default="hotel.png",
    )

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hotel_detail", args=[str(self.slug)])


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"), upload_to="hotels/gallery/", default="hotel.png"
    )
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Hotel Image")
        verbose_name_plural = _("Hotel Images")

    def __str__(self):
        return f"{self.hotel.name} - {self.caption}"


# Restaurant Models
class Restaurant(models.Model):
    name = models.CharField(_("Restaurant Name"), max_length=255)
    slug = AutoSlugField(populate_from="name", default="", unique=True)
    address = models.CharField(_("Address"), max_length=500)
    description = models.TextField(_("Description"))
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=5)
    price_range = models.DecimalField(_("Price Range"), max_digits=10, decimal_places=2)

    # Table Types
    has_family_tables = models.BooleanField(_("Family Tables"), default=False)
    has_business_tables = models.BooleanField(_("Business Tables"), default=False)
    has_private_tables = models.BooleanField(_("Private Tables"), default=False)

    # Menu Categories
    has_hot_dishes = models.BooleanField(_("Hot Dishes"), default=False)
    has_cold_dishes = models.BooleanField(_("Cold Dishes"), default=False)
    has_beverages = models.BooleanField(_("Beverages"), default=False)
    has_desserts = models.BooleanField(_("Desserts"), default=False)
    has_salads = models.BooleanField(_("Salads"), default=False)

    main_image = models.ImageField(
        _("Main Image"),
        upload_to="restaurants/main/",
        null=True,
        blank=True,
        default="restaurant.png",
    )

    class Meta:
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_detail", args=[str(self.slug)])


# Car Rental Agency Models
class CarRentalAgency(models.Model):
    name = models.CharField(_("Agency Name"), max_length=255)
    slug = AutoSlugField(populate_from="name", default="", unique=True)
    address = models.CharField(_("Address"), max_length=500)
    description = models.TextField(_("Description"))
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=5)

    # Services
    has_24hr_service = models.BooleanField(_("24/7 Service"), default=False)
    has_driver_service = models.BooleanField(_("Driver Service"), default=False)
    has_airport_pickup = models.BooleanField(_("Airport Pickup"), default=False)
    has_long_term_rental = models.BooleanField(_("Long Term Rental"), default=False)
    has_short_term_rental = models.BooleanField(_("Short Term Rental"), default=False)
    has_full_insurance = models.BooleanField(_("Full Insurance"), default=False)

    main_image = models.ImageField(
        _("Main Image"),
        upload_to="agencies/main/",
        null=True,
        blank=True,
        default="agency.png",
    )

    class Meta:
        verbose_name = _("Car Rental Agency")
        verbose_name_plural = _("Car Rental Agencies")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("car_rental_agency_detail", args=[str(self.slug)])


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ("auto", _("Automatic")),
        ("manual", _("Manual")),
    ]

    agency = models.ForeignKey(
        CarRentalAgency, related_name="cars", on_delete=models.CASCADE
    )
    brand = models.CharField(_("Brand"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    year = models.IntegerField(_("Year"))
    transmission = models.CharField(
        _("Transmission"), max_length=10, choices=TRANSMISSION_CHOICES
    )
    driver_cost_per_day = models.DecimalField(
        _("تسعيرة الركوب مع سائق"), max_digits=5, decimal_places=2, default=0
    )
    with_driver = models.BooleanField(_("مع سائق"), default=False)
    price_per_day = models.DecimalField(
        _("Price per Day"), max_digits=10, decimal_places=2
    )
    is_available = models.BooleanField(_("Available"), default=True)
    image = models.ImageField(
        _("Image"), upload_to="cars/", null=True, blank=True, default="car.png"
    )

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


# Restaurant Models
class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(_("Image"), upload_to="restaurants/gallery/")
    caption = models.CharField(
        _("Caption"), max_length=255, blank=True, default="restaurant.png"
    )

    class Meta:
        verbose_name = _("Restaurant Image")
        verbose_name_plural = _("Restaurant Images")

    def __str__(self):
        return f"{self.restaurant.name} - {self.caption}"


# Car Agency Models
class CarAgencyImage(models.Model):
    agency = models.ForeignKey(
        "CarRentalAgency", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        _("Image"), upload_to="agencies/gallery/", default="agency.png"
    )
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Agency Image")
        verbose_name_plural = _("Agency Images")

    def __str__(self):
        return f"{self.agency.name} - {self.caption}"


# Hotel Room Models
class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ("single", _("Single")),
        ("double", _("Double")),
        ("suite", _("Suite")),
        ("family", _("Family")),
        ("deluxe", _("Deluxe")),
    ]

    hotel = models.ForeignKey(Hotel, related_name="rooms", on_delete=models.CASCADE)
    room_type = models.CharField(
        _("Room Type"), max_length=20, choices=ROOM_TYPE_CHOICES
    )
    room_number = models.CharField(_("Room Number"), max_length=10)
    floor = models.IntegerField(_("Floor"))
    capacity = models.IntegerField(_("Capacity"))
    price_per_night = models.DecimalField(
        _("Price per Night"), max_digits=10, decimal_places=2
    )
    size_sqm = models.IntegerField(_("Size (m²)"))
    is_available = models.BooleanField(_("Available"), default=True)

    # Room Amenities
    has_air_conditioning = models.BooleanField(_("Air Conditioning"), default=False)
    has_heating = models.BooleanField(_("Heating"), default=False)
    has_minibar = models.BooleanField(_("Minibar"), default=False)
    has_tv = models.BooleanField(_("TV"), default=False)
    has_safe = models.BooleanField(_("Safe"), default=False)
    has_private_bathroom = models.BooleanField(_("Private Bathroom"), default=True)
    has_sea_view = models.BooleanField(_("Sea View"), default=False)
    has_balcony = models.BooleanField(_("Balcony"), default=False)

    image = models.ImageField(
        _("Image"), upload_to="rooms/", null=True, blank=True, default="room.png"
    )
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        unique_together = ["hotel", "room_number"]

    def __str__(self):
        return f"{self.hotel.name} - {self.get_room_type_display()} {self.room_number}"


# Restaurant Menu Models
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("main", _("Main Dish")),
        ("appetizer", _("Appetizer")),
        ("dessert", _("Dessert")),
        ("beverage", _("Beverage")),
        ("salad", _("Salad")),
    ]

    restaurant = models.ForeignKey(
        Restaurant, related_name="menu_items", on_delete=models.CASCADE
    )
    name = models.CharField(_("Dish Name"), max_length=255)
    category = models.CharField(_("Category"), max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    is_available = models.BooleanField(_("Available"), default=True)
    is_vegetarian = models.BooleanField(_("Vegetarian"), default=False)
    is_vegan = models.BooleanField(_("Vegan"), default=False)
    is_gluten_free = models.BooleanField(_("Gluten Free"), default=False)
    spiciness_level = models.IntegerField(
        _("Spiciness Level"), choices=[(i, i) for i in range(6)], default=0
    )
    preparation_time = models.IntegerField(_("Preparation Time (minutes)"), default=15)
    calories = models.IntegerField(_("Calories"), null=True, blank=True)

    image = models.ImageField(
        _("Image"), upload_to="menu_items/", null=True, blank=True, default="food.png"
    )

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"), upload_to="rooms/gallery/", default="room.png"
    )
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Room Image")
        verbose_name_plural = _("Room Images")

    def __str__(self):
        return f"{self.room.hotel.name} - Room {self.room.room_number} - {self.caption}"


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(
        MenuItem, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        _("Image"), upload_to="menu_items/gallery/", default="food.png"
    )
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Menu Item Image")
        verbose_name_plural = _("Menu Item Images")

    def __str__(self):
        return (
            f"{self.menu_item.restaurant.name} - {self.menu_item.name} - {self.caption}"
        )


# reservations
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("pending", _("Pending")),
            ("confirmed", _("Confirmed")),
            ("cancelled", _("Cancelled")),
            ("completed", _("Completed")),
        ],
        default="pending",
    )

    class Meta:
        abstract = True


class RestaurantReservation(BaseReservation):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="restaurants_reservations"
    )
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    table_type = models.CharField(
        _("Table Type"), max_length=50
    )  # e.g., 'طاولة ثنائية'

    menu_items = models.ManyToManyField(
        MenuItem, through="ReservationMenuItem", related_name="menuitems_reservations"
    )

    class Meta:
        verbose_name = _("Restaurant Reservation")
        verbose_name_plural = _("Restaurant Reservations")


class ReservationMenuItem(models.Model):
    reservation = models.ForeignKey(RestaurantReservation, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("reservation", "menu_item")

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for {self.reservation.id}"


class CarReservation(BaseReservation):
    agency = models.ForeignKey(
        "CarRentalAgency",
        on_delete=models.CASCADE,
        related_name="car_agency_reservations",
    )
    start_date = models.DateField()
    end_date = models.DateField(_("End Date"))
    car_brand = models.CharField(_("Car Brand"), max_length=100)  # e.g., 'DACIA'
    car_type = models.CharField(max_length=100)  # e.g., 'سيارة اقتصادية'

    # Additional options
    with_driver = models.BooleanField(default=False)
    insurance_type = models.CharField(
        max_length=50,
        choices=[
            ("basic", _("Basic")),
            ("full", _("Full Coverage")),
        ],
    )

    cars = models.ManyToManyField(
        Car, through="ReservationCar", related_name="car_reservations"
    )

    class Meta:
        verbose_name = _("Car Reservation")
        verbose_name_plural = _("Car Reservations")


class ReservationCar(models.Model):
    reservation = models.ForeignKey(CarReservation, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("reservation", "car")

    def __str__(self):
        return f"{self.car.brand} {self.car.model} for {self.reservation.id}"


class HotelReservation(BaseReservation):
    hotel = models.ForeignKey(
        "Hotel", on_delete=models.CASCADE, related_name="hotel_reservations"
    )
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField()

    # Additional services
    has_swimming_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_outdoor_area = models.BooleanField(default=False)

    rooms = models.ManyToManyField(
        Room, through="ReservationRoom", related_name="room_reservations"
    )

    class Meta:
        verbose_name = _("Hotel Reservation")
        verbose_name_plural = _("Hotel Reservations")


class ReservationRoom(models.Model):
    reservation = models.ForeignKey(HotelReservation, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("reservation", "room")

    def __str__(self):
        return (
            f"{self.room.room_type} {self.room.room_number} for {self.reservation.id}"
        )

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
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=0)
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
        _("Main Image"), upload_to="hotels/main/", null=True, blank=True
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
    image = models.ImageField(_("Image"), upload_to="hotels/gallery/")
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Hotel Image")
        verbose_name_plural = _("Hotel Images")

    def __str__(self):
        return f"{self.hotel.name} - {self.caption}"


# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


# Restaurant Models
class Restaurant(models.Model):
    name = models.CharField(_("Restaurant Name"), max_length=255)
    slug = AutoSlugField(populate_from="name", default="", unique=True)
    address = models.CharField(_("Address"), max_length=500)
    description = models.TextField(_("Description"))
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=0)
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
        _("Main Image"), upload_to="restaurants/main/", null=True, blank=True
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
    rating = models.DecimalField(_("Rating"), max_digits=2, decimal_places=1, default=0)

    # Services
    has_24hr_service = models.BooleanField(_("24/7 Service"), default=False)
    has_driver_service = models.BooleanField(_("Driver Service"), default=False)
    has_airport_pickup = models.BooleanField(_("Airport Pickup"), default=False)
    has_long_term_rental = models.BooleanField(_("Long Term Rental"), default=False)
    has_short_term_rental = models.BooleanField(_("Short Term Rental"), default=False)
    has_full_insurance = models.BooleanField(_("Full Insurance"), default=False)

    main_image = models.ImageField(
        _("Main Image"), upload_to="agencies/main/", null=True, blank=True
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
    price_per_day = models.DecimalField(
        _("Price per Day"), max_digits=10, decimal_places=2
    )
    is_available = models.BooleanField(_("Available"), default=True)
    image = models.ImageField(_("Image"), upload_to="cars/", null=True, blank=True)

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
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

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
    image = models.ImageField(_("Image"), upload_to="agencies/gallery/")
    caption = models.CharField(_("Caption"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Agency Image")
        verbose_name_plural = _("Agency Images")

    def __str__(self):
        return f"{self.agency.name} - {self.caption}"

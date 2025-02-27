# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class BaseReservationForm(forms.ModelForm):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class HotelReservationForm(BaseReservationForm):
    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label=_("الغرف"),
    )

    class Meta:
        model = HotelReservation
        fields = [
            "check_in",
            "check_out",
            "number_of_guests",
            "has_swimming_pool",
            "has_gym",
            "has_outdoor_area",
            "rooms",
        ]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "number_of_guests": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }
        labels = {
            "check_in": _("تاريخ تسجيل الدخول"),
            "check_out": _("تاريخ تسجيل الخروج"),
            "number_of_guests": _("عدد الضيوف"),
            "has_swimming_pool": _("مع مسبح"),
            "has_gym": _("مع صالة رياضية"),
            "has_outdoor_area": _("مع منطقة خارجية"),
        }

    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop("hotel", None)
        super().__init__(*args, **kwargs)
        if hotel:
            self.fields["rooms"].queryset = Room.objects.filter(hotel=hotel)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out and check_in >= check_out:
            raise forms.ValidationError(_("Check-out date must be after check-in date"))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for room in self.cleaned_data["rooms"]:
                print(room)
                ReservationRoom.objects.create(
                    reservation=instance, room=room, quantity=1
                )
        return instance


class RestaurantReservationForm(BaseReservationForm):
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label=_("قائمة الطعام"),
    )

    class Meta:
        model = RestaurantReservation
        fields = [
            "reservation_date",
            "reservation_time",
            "table_type",
            "menu_items",
        ]
        widgets = {
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "reservation_time": forms.TimeInput(attrs={"type": "time"}),
            "table_type": forms.Select(
                choices=[
                    ("double", _("طاولة ثنائية")),
                    ("family", _("طاولة عائلية")),
                    ("large", _("طاولة كبيرة")),
                ]
            ),
        }
        labels = {
            "reservation_date": _("تاريخ الحجز"),
            "reservation_time": _("وقت الحجز"),
            "table_type": _("نوع الطاولة"),
        }

    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop("restaurant", None)
        super().__init__(*args, **kwargs)
        if restaurant:
            self.fields["menu_items"].queryset = MenuItem.objects.filter(
                restaurant=restaurant
            )

    def clean(self):
        cleaned_data = super().clean()
        # Add validation to ensure at least one dish is ordered
        if not cleaned_data.get("menu_items"):
            raise forms.ValidationError(_("Please order at least one dish"))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for menu_item in self.cleaned_data["menu_items"]:
                ReservationMenuItem.objects.create(
                    reservation=instance, menu_item=menu_item, quantity=1
                )
        return instance


class CarReservationForm(BaseReservationForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label=_("السيارات"),
    )

    class Meta:
        model = CarReservation
        fields = [
            "start_date",
            "end_date",
            "with_driver",
            "insurance_type",
            "cars",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "insurance_type": forms.Select(
                choices=[
                    ("basic", _("تأمين أساسي")),
                    ("full", _("تغطية شاملة")),
                ]
            ),
        }
        labels = {
            "start_date": _("تاريخ البداية"),
            "end_date": _("تاريخ النهاية"),
            "with_driver": _("مع سائق"),
            "insurance_type": _("نوع التأمين"),
        }

    def __init__(self, *args, **kwargs):
        agency = kwargs.pop("agency", None)
        super().__init__(*args, **kwargs)
        if agency:
            # Only show cars that support with_driver if with_driver is selected
            self.fields["cars"].queryset = Car.objects.filter(agency=agency)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        with_driver = cleaned_data.get("with_driver")
        cars = cleaned_data.get("cars")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(_("End date must be after start date"))

        # Validate that selected cars support driver service if with_driver is selected
        if with_driver and cars:
            for car in cars:
                if not car.with_driver:
                    raise forms.ValidationError(
                        _(f"السيارة من الموديل {car.model}  لا تدعم خدمة السائق , هي للكراء فقط يرجى إختيار سيارة أخرى مخصصة لذلك او تعطيل خاصية السائق لاخيتار السيارات التي تريد كراءها ")
                    )

        return cleaned_data


# Form Factory to get the appropriate form based on listing type
def get_reservation_form(listing_type, data=None, **kwargs):
    form_mapping = {
        "hotels": HotelReservationForm,
        "restaurants": RestaurantReservationForm,
        "car-rental-agencies": CarReservationForm,
    }

    FormClass = form_mapping.get(listing_type)
    if not FormClass:
        raise ValueError(f"Invalid listing type: {listing_type}")

    # Filter kwargs based on form type
    filtered_kwargs = {}
    if listing_type == "hotels" and "hotel" in kwargs:
        filtered_kwargs["hotel"] = kwargs["hotel"]
    elif listing_type == "restaurants" and "restaurant" in kwargs:
        filtered_kwargs["restaurant"] = kwargs["restaurant"]
    elif listing_type == "car-rental-agencies" and "agency" in kwargs:
        filtered_kwargs["agency"] = kwargs["agency"]

    if data:
        return FormClass(data=data, **filtered_kwargs)
    return FormClass(**filtered_kwargs)

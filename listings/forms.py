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
        queryset=Room.objects.none(), widget=forms.CheckboxSelectMultiple, required=True
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
                ReservationRoom.objects.create(
                    reservation=instance, room=room, quantity=1
                )
        return instance


class RestaurantReservationForm(BaseReservationForm):
    menu_items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
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
        queryset=Car.objects.none(), widget=forms.CheckboxSelectMultiple, required=True
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

    def __init__(self, *args, **kwargs):
        agency = kwargs.pop("agency", None)
        super().__init__(*args, **kwargs)
        if agency:
            self.fields["cars"].queryset = Car.objects.filter(agency=agency)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(_("End date must be after start date"))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for car in self.cleaned_data["cars"]:
                ReservationCar.objects.create(reservation=instance, car=car, quantity=1)
        return instance


# Form Factory to get the appropriate form based on listing type
def get_reservation_form(listing_type, **kwargs):
    form_mapping = {
        "hotels": HotelReservationForm,
        "restaurants": RestaurantReservationForm,
        "car-rental-agencies": CarReservationForm,
    }
    return form_mapping.get(listing_type)(**kwargs)


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import get_reservation_form
from .models import Hotel, Restaurant, CarRentalAgency


def make_reservation(request, listing_type, slug):
    if listing_type == "hotels":
        listing = get_object_or_404(Hotel, slug=slug)
    elif listing_type == "restaurants":
        listing = get_object_or_404(Restaurant, slug=slug)
    elif listing_type == "car-rental-agencies":
        listing = get_object_or_404(CarRentalAgency, slug=slug)
    else:
        raise ValueError("Invalid listing type")

    FormClass = get_reservation_form(
        listing_type,
        hotel=listing if listing_type == "hotels" else None,
        restaurant=listing if listing_type == "restaurants" else None,
        agency=listing if listing_type == "car-rental-agencies" else None,
    )

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect("reservation_confirmation", reservation.id)
    else:
        form = FormClass()

    return render(
        request,
        "reservations/reservation_form.html",
        {"form": form, "listing_type": listing_type, "listing": listing},
    )


# payment forms
# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Payment, SavedCard


class PaymentForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ("visa", _("بطاقة فيزا / باي بال")),
        ("bank", _("البنك")),
        ("baridimob", _("بريدي موب")),
        ("cash", _("نقدا")),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect, initial="visa"
    )

    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "رقم البطاقة", "class": "card-input"}
        ),
    )

    card_holder = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "اسم حامل البطاقة", "class": "card-input"}
        ),
    )

    expiry_month = forms.ChoiceField(
        required=False,
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        widget=forms.Select(attrs={"class": "select-date"}),
    )

    expiry_year = forms.ChoiceField(
        required=False,
        choices=[(str(i)[-2:], str(i)[-2:]) for i in range(2024, 2035)],
        widget=forms.Select(attrs={"class": "select-date"}),
    )

    cvv = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "card-input", "maxlength": "3"}),
    )

    save_card = forms.BooleanField(
        required=False, initial=False, label=_("حفظ هذه البطاقة للمعاملات المستقبلية")
    )

    class Meta:
        model = Payment
        fields = ["payment_method"]

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")

        if payment_method == "visa":
            required_fields = [
                "card_number",
                "card_holder",
                "expiry_month",
                "expiry_year",
                "cvv",
            ]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, _("هذا الحقل مطلوب"))

        return cleaned_data

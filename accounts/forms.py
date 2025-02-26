# accounts/forms.py

from django import forms

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import *


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "address",
            "profile_picture",
            "language",
            "currency",
            "booking_notifications",
            "promotional_notifications",
            "reminder_notifications",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any custom initialization here, such as adding CSS classes
        for field in self.fields:
            # if it is either language or currency field add w-25 and me-auto to them without overriding
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "form-control"
                        if field not in ["language", "currency"]
                        else "form-control w-25 me-auto"
                    )
                }
            )

        # Customize the widget for boolean fields (checkboxes)
        for boolean_field in [
            "booking_notifications",
            "promotional_notifications",
            "reminder_notifications",
        ]:
            self.fields[boolean_field].widget = forms.CheckboxInput(
                # add the bs5 toggle class to them
                attrs={"class": "form-check-input me-auto"}
            )

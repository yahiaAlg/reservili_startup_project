# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import SavedCard, encrypt_card_number


class SavedCardForm(forms.ModelForm):
    class Meta:
        model = SavedCard
        fields = [
            "card_type",
            "card_holder",
            "last_four",
            "expiry_month",
            "expiry_year",
            "is_default",
        ]
        widgets = {
            "expiry_month": forms.Select(
                choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)]
            ),
            "expiry_year": forms.Select(
                choices=[(str(i)[-2:], str(i)[-2:]) for i in range(2024, 2035)]
            ),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.encrypted_card_number = encrypt_card_number(
                self.cleaned_data["card_number"]
            )
            instance.save()
        return instance

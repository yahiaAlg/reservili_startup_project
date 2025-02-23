from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class PaymentMethodForm(forms.Form):
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(is_active=True),
        widget=forms.HiddenInput(),
    )


# payments/forms.py
class PaymentForm(forms.ModelForm):

    use_saved_card = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "رقم البطاقة",
                "class": "card-input text-end",
                "type": "tel",
            }
        ),
    )

    card_holder = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "اسم حامل البطاقة",
                "class": "card-input text-end",
            }
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
        widget=forms.TextInput(
            attrs={"maxlength": "3", "type": "tel", "class": "card-input"}
        ),
    )

    save_card = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Payment
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.reservation = kwargs.pop("reservation", None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.saved_cards.exists():
            self.fields["saved_card"] = forms.ModelChoiceField(
                queryset=self.user.saved_cards.all(),
                required=False,
                empty_label=_("Select a saved card"),
                widget=forms.Select(attrs={"class": "form-select"}),
            )

    def clean(self):
        cleaned_data = super().clean()

        use_saved_card = cleaned_data.get("use_saved_card")
        saved_card = cleaned_data.get("saved_card")

        if use_saved_card and not saved_card:
            self.add_error("saved_card", _("الرجاء تحديد بطاقة محفوظة"))

        return cleaned_data


class SavedCardForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "card-input",
                "placeholder": "رقم البطاقة",
            }
        ),
    )

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
            "card_type": forms.Select(attrs={"class": "form-select"}),
            "card_holder": forms.TextInput(attrs={"class": "card-input"}),
            "last_four": forms.TextInput(attrs={"class": "card-input"}),
            "expiry_month": forms.Select(
                choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
                attrs={"class": "select-date form-select"},
            ),
            "expiry_year": forms.Select(
                choices=[(str(i)[-2:], str(i)[-2:]) for i in range(2024, 2035)],
                attrs={"class": "select-date form-select"},
            ),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.encrypted_card_number = encrypt_card_number(
                self.cleaned_data["card_number"]
            )
            instance.save()
        return instance

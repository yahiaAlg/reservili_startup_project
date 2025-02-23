from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Payment, SavedCard, encrypt_card_number


# payments/forms.py
class PaymentForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ("visa", _("بطاقة فيزا / باي بال")),
        ("mastercard", _("ماستر كارد")),
        ("bank", _("البنك")),
        ("baridimob", _("بريدي موب")),
        ("cash", _("نقدا")),
    ]

    use_saved_card = forms.BooleanField(required=False, initial=False)
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect, initial="visa"
    )
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "رقم البطاقة", "class": "card-input", "type": "tel"}
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
    )
    expiry_year = forms.ChoiceField(
        required=False,
        choices=[(str(i)[-2:], str(i)[-2:]) for i in range(2024, 2035)],
    )
    cvv = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"maxlength": "3", "type": "tel"}),
    )
    save_card = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Payment
        fields = ["payment_method"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.reservation = kwargs.pop("reservation", None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.saved_cards.exists():
            self.fields["saved_card"] = forms.ModelChoiceField(
                queryset=self.user.saved_cards.all(),
                required=False,
                empty_label=_("Select a saved card"),
            )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")
        use_saved_card = cleaned_data.get("use_saved_card")
        saved_card = cleaned_data.get("saved_card")

        if payment_method in ["visa", "mastercard"] and not use_saved_card:
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

        if use_saved_card and not saved_card:
            self.add_error("saved_card", _("Please select a saved card"))

        return cleaned_data


class SavedCardForm(forms.ModelForm):
    # add card number attribute
    card_number = forms.CharField(
        max_length=16, widget=forms.TextInput(attrs={"type": "tel"})
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

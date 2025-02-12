from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Payment, SavedCard, encrypt_card_number


class PaymentForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ("visa", _("بطاقة فيزا / باي بال")),
        ("mastercard", _("ماستر كارد")),
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
        fields = ["payment_method", "amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["saved_card"] = forms.ModelChoiceField(
                queryset=SavedCard.objects.filter(user=self.user),
                required=False,
                label=_("اختر بطاقة محفوظة"),
            )

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")

        if payment_method in ["visa", "mastercard"]:
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

    def save(self, commit=True):
        instance = super().save(commit=False)
        payment_method = self.cleaned_data.get("payment_method")

        if payment_method in ["visa", "mastercard"]:
            card_number = self.cleaned_data.get("card_number")
            card_holder = self.cleaned_data.get("card_holder")
            expiry_month = self.cleaned_data.get("expiry_month")
            expiry_year = self.cleaned_data.get("expiry_year")
            cvv = self.cleaned_data.get("cvv")

            if self.cleaned_data.get("save_card"):
                SavedCard.objects.create(
                    user=self.user,
                    card_type=payment_method,
                    card_holder=card_holder,
                    last_four=card_number[-4:],
                    encrypted_card_number=encrypt_card_number(card_number),
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    is_default=True,
                )

        if commit:
            instance.save()
        return instance


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

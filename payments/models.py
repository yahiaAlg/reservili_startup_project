from django.db import models

# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator

import hashlib

# reservations
from django.contrib.auth import get_user_model


User = get_user_model()


# a payement method can be related to many users and the user can have many payment methods
class PaymentMethod(models.Model):

    name = models.CharField("Payment Method Name", max_length=50)
    is_active = models.BooleanField("Active", default=True)
    is_default = models.BooleanField("Default", default=False)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name


class SavedCard(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_cards")
    card_type = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="saved_cards"
    )
    card_holder = models.CharField("Card Holder Name", max_length=255)
    last_four = models.CharField("Last 4 Digits", max_length=4)
    encrypted_card_number = models.CharField(max_length=255, blank=True)
    expiry_month = models.CharField(
        "Expiry Month", max_length=2, validators=[MinLengthValidator(2)]
    )
    expiry_year = models.CharField(
        "Expiry Year", max_length=2, validators=[MinLengthValidator(2)]
    )
    is_default = models.BooleanField("Default Card", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Saved Card"
        verbose_name_plural = "Saved Cards"

    def __str__(self):
        return f"{self.card_type} **** {self.last_four}"

    def save(self, *args, **kwargs):
        if self.is_default:
            SavedCard.objects.filter(user=self.user).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)


class Payment(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    amount = models.DecimalField("Amount", max_digits=10, decimal_places=2)
    saved_card = models.ForeignKey(
        SavedCard, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        "Status", max_length=20, choices=PAYMENT_STATUS, default="pending"
    )
    transaction_id = models.CharField("Transaction ID", max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relation to reservation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reservation = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment {self.transaction_id}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Payment)
def handle_payment_status_change(sender, instance, created, **kwargs):
    if created:
        # Trigger payment processing
        pass
    elif instance.status == "completed":
        # Update reservation status
        reservation = instance.reservation
        if reservation:
            reservation.status = "confirmed"
            reservation.save()
    elif instance.status == "failed":
        # Handle failed payment
        reservation = instance.reservation
        if reservation:
            reservation.status = "pending"
            reservation.save()


# Utility function for card encryption (example)
def encrypt_card_number(card_number):
    return hashlib.sha256(card_number.encode()).hexdigest()

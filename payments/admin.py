import hashlib
from .models import *

# Register your models here.
# Admin configuration
from django.contrib import admin


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "is_default")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(SavedCard)
class SavedCardAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "card_type",
        "last_four",
        "expiry_month",
        "expiry_year",
        "is_default",
    )
    list_filter = ("card_type", "is_default")
    search_fields = ("user__username", "card_holder")
    readonly_fields = ("encrypted_card_number", "last_four")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "amount",
        "saved_card",
        "status",
        "created_at",
    )
    list_filter = ("status", "saved_card", "created_at")
    search_fields = ("transaction_id", "user__username")
    readonly_fields = ("transaction_id", "created_at")
    date_hierarchy = "created_at"


# Utility function for card encryption (example)
def encrypt_card_number(card_number):
    return hashlib.sha256(card_number.encode()).hexdigest()

from django.contrib import admin

from accounts.models import *

# Register your models here.
# Admin configuration


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "language", "currency")
    list_filter = ("language", "currency", "booking_notifications")
    search_fields = ("user__username", "phone_number", "address")
    readonly_fields = ("created_at", "updated_at")


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ("user", "content_type", "created_at")
#     list_filter = ("content_type", "created_at")
#     search_fields = ("user__username",)
#     date_hierarchy = "created_at"

# notifications/admin.py
from django.contrib import admin
from .models import Notification, UserNotification


class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    extra = 0
    readonly_fields = ("user", "is_read", "read_at")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "action", "created_at", "display_users")
    list_filter = ("action", "created_at")
    search_fields = ("listing_title", "message")
    ordering = ("-created_at",)
    inlines = [UserNotificationInline]

    def display_users(self, obj):
        # Show a comma-separated list of users associated with this notification.
        return ", ".join([str(un.user) for un in obj.user_notifications.all()])

    display_users.short_description = "Users"


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "notification", "is_read", "read_at")
    list_filter = ("is_read", "notification__action")
    search_fields = ("user__username", "notification__listing_title")


# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import CarouselSlide


@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "title", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    list_display_links = ["thumbnail", "title"]
    search_fields = ["title", "subtitle"]
    list_filter = ["is_active", "created_at"]
    readonly_fields = ["image_preview", "created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("title", "subtitle", "image", "image_preview")}),
        (
            "Button Options",
            {"fields": ("button_text", "button_link"), "classes": ("collapse",)},
        ),
        ("Display Settings", {"fields": ("order", "is_active")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 30px; object-fit: cover;"/>',
                obj.image.url,
            )
        return "No Image"

    thumbnail.short_description = "Preview"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; height: auto;"/>', obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"

    class Media:
        css = {"all": ("admin/css/carousel_admin.css",)}

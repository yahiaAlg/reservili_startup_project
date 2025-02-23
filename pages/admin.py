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

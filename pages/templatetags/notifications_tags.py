# notifications/templatetags/notifications_tags.py
from django import template
from ..models import UserNotification

register = template.Library()


@register.inclusion_tag("partials/_notifications.html", takes_context=True)
def show_notifications(context):
    request = context["request"]
    # Retrieve the latest 5 notifications for the logged in user
    user_notifications = (
        UserNotification.objects.filter(user=request.user)
        .select_related("notification")
        .order_by("-notification__created_at")[:5]
    )
    unread_count = UserNotification.objects.filter(
        user=request.user, is_read=False
    ).count()
    return {
        "user_notifications": user_notifications,
        "notification_badge": unread_count,
    }

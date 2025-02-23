# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Notification(models.Model):
    ACTION_CHOICES = (
        ("created", "Created"),
        ("updated", "Updated"),
        ("deleted", "Deleted"),
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    listing_title = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing_title} {self.action} at {self.created_at}"


class UserNotification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notifications"
    )
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="user_notifications"
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "notification")
        ordering = ["-notification__created_at"]

    def __str__(self):
        return f"{self.user} - {self.notification} (Read: {self.is_read})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} favorited {self.content_object}"


# notifications/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from listings.models import Hotel, Restaurant, CarRentalAgency

User = get_user_model()


def create_user_notifications(instance, action):
    # Create a Notification record (if not already created)
    notification = Notification.objects.create(
        content_object=instance,
        listing_title=getattr(instance, "name", str(instance)),
        action=action,
        message=f"{getattr(instance, 'name', 'Listing')} has been {action}.",
    )
    # For example, associate this notification with all active users.
    # You can filter this queryset as needed.
    for user in User.objects.all():
        UserNotification.objects.create(user=user, notification=notification)


# --- Hotel signals ---
@receiver(post_save, sender=Hotel)
def hotel_post_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    create_user_notifications(instance, action)


@receiver(post_delete, sender=Hotel)
def hotel_post_delete(sender, instance, **kwargs):
    create_user_notifications(instance, "deleted")


# --- Restaurant signals ---
@receiver(post_save, sender=Restaurant)
def restaurant_post_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    create_user_notifications(instance, action)


@receiver(post_delete, sender=Restaurant)
def restaurant_post_delete(sender, instance, **kwargs):
    create_user_notifications(instance, "deleted")


# --- Car Rental Agency signals ---
@receiver(post_save, sender=CarRentalAgency)
def car_agency_post_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    create_user_notifications(instance, action)


@receiver(post_delete, sender=CarRentalAgency)
def car_agency_post_delete(sender, instance, **kwargs):
    create_user_notifications(instance, "deleted")

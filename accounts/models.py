# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# importing  settings

# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Profile(models.Model):
    LANGUAGE_CHOICES = [
        ("ar", _("Arabic")),
        ("en", _("English")),
        ("fr", _("French")),
    ]

    CURRENCY_CHOICES = [
        ("DZD", _("Algerian Dinar")),
        ("USD", _("US Dollar")),
        ("EUR", _("Euro")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True)
    address = models.TextField(_("Address"), blank=True)
    profile_picture = models.ImageField(
        _("Profile Picture"), upload_to="profiles/", null=True, blank=True
    )

    # Preferences
    language = models.CharField(
        _("Language"), max_length=2, choices=LANGUAGE_CHOICES, default="ar"
    )
    currency = models.CharField(
        _("Currency"), max_length=3, choices=CURRENCY_CHOICES, default="DZD"
    )

    # Notification preferences
    booking_notifications = models.BooleanField(
        _("Booking Notifications"), default=True
    )
    promotional_notifications = models.BooleanField(
        _("Promotional Notifications"), default=True
    )
    reminder_notifications = models.BooleanField(
        _("Reminder Notifications"), default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile with a default profile picture
        Profile.objects.create(user=instance, profile_picture="/#")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, "profile"):
        # Create the profile with a default profile picture if it doesn't exist
        Profile.objects.create(user=instance, profile_picture="/#")
    instance.profile.save()

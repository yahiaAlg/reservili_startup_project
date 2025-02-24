from django.urls import path
from . import views


urlpatterns = [
    path(
        "notifications/mark_read/<int:notification_id>/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path("", views.index_view, name="index"),
    path("booking/", views.booking_view, name="booking"),
    path("bookmark/", views.bookmark_view, name="bookmark"),
    path(
        "cancel_reservation/<str:listing_type>/<int:reservation_id>/",
        views.cancel_reservation,
        name="cancel_reservation",
    ),
    # search
    path("agency-search/", views.agency_search, name="agency_search"),
    path("hotel-search/", views.hotel_search, name="hotel_search"),
    path("restaurant-search/", views.restaurant_search, name="restaurant_search"),
]

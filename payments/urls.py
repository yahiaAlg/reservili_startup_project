from django.urls import path
from . import views


urlpatterns = [
    path("cards/", views.manage_saved_cards, name="manage_saved_cards"),
    path("cards/add/", views.add_saved_card, name="add_saved_card"),
    path("cards/<int:card_id>/edit/", views.edit_saved_card, name="edit_saved_card"),
    path(
        "cards/<int:card_id>/delete/", views.delete_saved_card, name="delete_saved_card"
    ),
    path(
        "cards/<int:card_id>/toggle-default/",
        views.toggle_default_card,
        name="toggle_default_card",
    ),
]

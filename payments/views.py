from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import PaymentForm
from .models import (
    Payment,
    HotelReservation,
    RestaurantReservation,
    CarReservation,
    SavedCard,
    encrypt_card_number,
)


@login_required
def payment_view(request, listing_type, reservation_id):
    # Get the appropriate reservation model based on listing_type
    reservation_models = {
        "hotels": HotelReservation,
        "restaurants": RestaurantReservation,
        "car-rental-agencies": CarReservation,
    }

    ReservationModel = reservation_models.get(listing_type)
    if not ReservationModel:
        raise Http404("Invalid listing type")

    reservation = get_object_or_404(
        ReservationModel, id=reservation_id, user=request.user
    )

    if request.method == "POST":
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.amount = reservation.total_price
            payment.reservation = reservation

            # Handle card saving if requested
            if form.cleaned_data.get("save_card"):
                SavedCard.objects.create(
                    user=request.user,
                    card_type=form.cleaned_data["payment_method"],
                    card_holder=form.cleaned_data["card_holder"],
                    last_four=form.cleaned_data["card_number"][-4:],
                    encrypted_card_number=encrypt_card_number(
                        form.cleaned_data["card_number"]
                    ),
                    expiry_month=form.cleaned_data["expiry_month"],
                    expiry_year=form.cleaned_data["expiry_year"],
                    is_default=True,
                )

            payment.save()
            return redirect("payment_confirmation", payment_id=payment.id)
    else:
        form = PaymentForm(user=request.user)

    return render(
        request,
        "reservations/confirm_payment.html",
        {
            "form": form,
            "listing_type": listing_type,
            "object": reservation.hotel or reservation.restaurant or reservation.agency,
            "total_price": reservation.total_price,
        },
    )


@login_required
def payment_confirmation(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(
        request, "reservations/payment_confirmation.html", {"payment": payment}
    )


@login_required
@require_http_methods(["GET"])
def manage_saved_cards(request):
    context = {
        "saved_cards": SavedCard.objects.filter(user=request.user),
        "payment_methods": PaymentMethod.objects.filter(is_active=True),
        "form": SavedCardForm(),
    }
    return render(request, "payments/manage_saved_cards.html", context)


@login_required
@require_POST
def add_saved_card(request):
    form = SavedCardForm(request.POST)
    if form.is_valid():
        saved_card = form.save(commit=False)
        saved_card.user = request.user
        saved_card.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "Card added successfully",
                "card": {
                    "id": saved_card.id,
                    "card_type": saved_card.get_card_type_display(),
                    "last_four": saved_card.last_four,
                    "expiry_month": saved_card.expiry_month,
                    "expiry_year": saved_card.expiry_year,
                    "card_holder": saved_card.card_holder,
                    "is_default": saved_card.is_default,
                },
            }
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid form data", "errors": form.errors},
        status=400,
    )


@login_required
@require_http_methods(["GET", "POST"])
def edit_saved_card(request, card_id):
    saved_card = get_object_or_404(SavedCard, id=card_id, user=request.user)

    if request.method == "POST":
        form = SavedCardForm(request.POST, instance=saved_card)
        if form.is_valid():
            saved_card = form.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Card updated successfully",
                    "card": {
                        "id": saved_card.id,
                        "card_type": saved_card.get_card_type_display(),
                        "last_four": saved_card.last_four,
                        "expiry_month": saved_card.expiry_month,
                        "expiry_year": saved_card.expiry_year,
                        "card_holder": saved_card.card_holder,
                        "is_default": saved_card.is_default,
                    },
                }
            )
        return JsonResponse(
            {"status": "error", "message": "Invalid form data", "errors": form.errors},
            status=400,
        )

    # For GET requests, return the form HTML
    form = SavedCardForm(instance=saved_card)
    return render(
        request,
        "payments/partials/edit_card_form.html",
        {"form": form, "card_id": card_id},
    )


@login_required
@require_POST
def delete_saved_card(request, card_id):
    saved_card = get_object_or_404(SavedCard, id=card_id, user=request.user)
    saved_card.delete()
    return JsonResponse({"status": "success", "message": "Card deleted successfully"})


# Optional: Add a view to toggle card default status
@login_required
@require_POST
def toggle_default_card(request, card_id):
    saved_card = get_object_or_404(SavedCard, id=card_id, user=request.user)
    saved_card.is_default = not saved_card.is_default
    saved_card.save()
    return JsonResponse(
        {
            "status": "success",
            "message": "Card default status updated",
            "is_default": saved_card.is_default,
        }
    )

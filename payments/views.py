from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import PaymentForm
from listings.models import (
    HotelReservation,
    RestaurantReservation,
    CarReservation,
)

# messages
from django.contrib import messages


from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# payments/views.py
@login_required
def payment_view(request, listing_type, reservation_id):
    show_new_payment_forms = False
    if request.method == "GET" and request.GET.get("show_new_payment_forms", False):
        show_new_payment_forms = True
    # Map listing types to reservation models
    reservation_models = {
        "hotels": HotelReservation,
        "restaurants": RestaurantReservation,
        "car-rental-agencies": CarReservation,
    }
    reservation_types = {
        "hotels": "hotel",
        "restaurants": "restaurant",
        "car-rental-agencies": "car",
    }

    ReservationModel = reservation_models.get(listing_type)
    if not ReservationModel:
        raise Http404("Invalid listing type")

    reservation = get_object_or_404(
        ReservationModel, id=reservation_id, user=request.user
    )

    if request.method == "POST":
        if request.user.saved_cards.exists():
            selected_card_id = request.POST.get("selected_card_id")
            if selected_card_id:
                selected_card = request.user.saved_cards.get(id=selected_card_id)
                new_payment = Payment.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(reservation),
                    object_id=reservation.id,
                    amount=reservation.total_price,
                    card=selected_card,
                    payment_method="saved_card",
                )

                messages.success(request, "Payment successful")
                return redirect(
                    "reservation_confirmation",
                    reservation_type=reservation_types.get(listing_type),
                    reservation_id=reservation.id,
                )

        print("post method entered")
        payment_method_form = PaymentMethodForm(request.POST)
        payment_detail_form = PaymentForm(
            request.POST, user=request.user, reservation=reservation
        )
        if payment_method_form.is_valid() and payment_detail_form.is_valid():

            payment = payment_detail_form.save(commit=False)
            payment.user = request.user
            payment.amount = reservation.total_price

            # Get the selected payment method from the radio buttons
            payment_method_id = request.POST.get("paymentMethod")
            try:
                payment_method = PaymentMethod.objects.get(id=payment_method_id)
                payment.payment_method = payment_method
            except PaymentMethod.DoesNotExist:
                payment_method_form.add_error(
                    "payment_method", "Invalid payment method selected"
                )

                return render(
                    request,
                    "payments/confirm_payment.html",
                    {
                        "payment_detail_form": payment_detail_form,
                        "payment_method_form": payment_method_form,
                        "object": getattr(
                            reservation,
                            (
                                listing_type.rstrip("s")
                                if not listing_type == "car-rental-agencies"
                                else "agency"
                            ),
                        ),
                        "total_price": reservation.total_price,
                        "payment_methods": PaymentMethod.objects.filter(is_active=True),
                    },
                )

            # Set content type and object id for generic relation
            content_type = ContentType.objects.get_for_model(reservation)
            payment.content_type = content_type
            payment.object_id = reservation.id

            # Handle saved card usage
            if payment_detail_form.cleaned_data.get("use_saved_card"):
                payment.saved_card = payment_detail_form.cleaned_data["saved_card"]
            elif payment_detail_form.cleaned_data.get("save_card"):
                # Create new saved card
                saved_card = SavedCard.objects.create(
                    user=request.user,
                    card_type=payment_method,  # Use the selected payment method
                    card_holder=payment_detail_form.cleaned_data["card_holder"],
                    last_four=payment_detail_form.cleaned_data["card_number"][-4:],
                    encrypted_card_number=encrypt_card_number(
                        payment_detail_form.cleaned_data["card_number"]
                    ),
                    expiry_month=payment_detail_form.cleaned_data["expiry_month"],
                    expiry_year=payment_detail_form.cleaned_data["expiry_year"],
                )
                payment.saved_card = saved_card

            payment.status = "processing"  # Set initial status
            payment.save()

            # Update reservation status
            reservation.status = "pending"
            reservation.save()

            return redirect(
                "reservation_confirmation",
                reservation_type=reservation_types.get(listing_type),
                reservation_id=reservation.id,
            )

        else:
            # If form is invalid, return the form with errors in the messages

            for field, error in payment_detail_form.errors.items():
                print(f"{field}: {error}")
                messages.error(request, f"{field}: {error}")
            for field, error in payment_method_form.errors.items():
                print(f"{field}: {error}")
                messages.error(request, f"{field}: {error}")

            return redirect(
                "payment", reservation_id=reservation.id, listing_type=listing_type
            )
    else:
        payment_detail_form = PaymentForm(user=request.user, reservation=reservation)
        payment_method_form = PaymentMethodForm()

    return render(
        request,
        "payments/confirm_payment.html",
        {
            "form": payment_detail_form,
            "payment_method_form": payment_method_form,
            "object": getattr(
                reservation,
                (
                    listing_type.rstrip("s")
                    if not listing_type == "car-rental-agencies"
                    else "agency"
                ),
            ),
            "total_price": reservation.total_price,
            "listing_type": listing_type,
            "reservation_id": reservation.id,
            "payment_methods": PaymentMethod.objects.filter(is_active=True),
        },
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
        messages.success(
            request, "Card saved successfully. You can use it for future payments."
        )
        return redirect("manage_saved_cards")

    messages.error(request, "Failed to save card. Please try again.")
    return redirect("manage_saved_cards")


@login_required
@require_POST
def delete_saved_card(request, card_id):
    saved_card = get_object_or_404(SavedCard, id=card_id, user=request.user)
    saved_card.delete()
    messages.info(request, "Card deleted !.")
    return redirect("manage_saved_cards")


# Optional: Add a view to toggle card default status
@login_required
@require_POST
def toggle_default_card(request, card_id):
    # make the previous saved default card non default first
    prev_default_card = get_object_or_404(SavedCard, is_default=True, user=request.user)
    print(f"prev_default_card: {prev_default_card.id} {prev_default_card.is_default}")
    prev_default_card.is_default = not prev_default_card.is_default

    saved_card = get_object_or_404(SavedCard, id=card_id, user=request.user)
    saved_card.is_default = not saved_card.is_default
    print(f"saved_card: {saved_card.id} {saved_card.is_default} {saved_card .user.id}")
    saved_card.save()
    messages.info(request, "Card default status toggled !")
    return redirect("manage_saved_cards")

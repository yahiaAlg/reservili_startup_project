from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from listings.models import Restaurant, Hotel, CarRentalAgency
from .forms import *
from .models import *
import random


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("profile")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def settings_view(request):
    """
    View function to display the settings page with forms for updating user and profile information.
    """
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # Initialize forms with the current user and profile data
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
    }

    return render(request, "accounts/settings.html", context)


@login_required
def upload_profile_picture(request):
    if request.method == "POST":
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        user_profile.profile_picture = request.FILES.get("profile_picture")
        user_profile.save()
        messages.success(request, "Your profile picture has been updated!")
        return redirect("settings")
    return redirect("settings")


@login_required
def update_profile_info(request):
    if request.method == "POST":
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        # Update User email field
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update Profile fields
        user_profile.phone_number = request.POST.get("phone_number")
        user_profile.address = request.POST.get("address")
        user_profile.save()

        messages.success(request, "Your profile information has been updated!")
        return redirect("settings")

    return redirect("index")


@login_required
def update_preferences(request):
    if request.method == "POST":
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        # Update Profile preferences
        user_profile.language = request.POST.get("language")
        user_profile.currency = request.POST.get("currency")
        user_profile.save()

        messages.success(request, "Your preferences have been updated!")
        return redirect("settings")

    return redirect("index")


@login_required
def update_notifications(request):
    if request.method == "POST":
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        # Update Profile notification preferences
        user_profile.booking_notifications = "booking_notifications" in request.POST
        user_profile.promotional_notifications = (
            "promotional_notifications" in request.POST
        )
        user_profile.reminder_notifications = "reminder_notifications" in request.POST
        user_profile.save()

        messages.success(request, "Your notification preferences have been updated!")
        return redirect("settings")

    return redirect("index")


@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    # Get random 4 samples of each listing category
    hotels = list(Hotel.objects.all())
    random.shuffle(hotels)
    recent_hotels = hotels[:4]

    restaurants = list(Restaurant.objects.all())
    random.shuffle(restaurants)
    recent_restaurants = restaurants[:4]

    car_agencies = list(CarRentalAgency.objects.all())
    random.shuffle(car_agencies)
    recent_car_agencies = car_agencies[:4]

    if user_profile:
        context = {
            "user_profile": user_profile,
            "recent_hotels": recent_hotels,
            "recent_restaurants": recent_restaurants,
            "recent_car_agencies": recent_car_agencies,
        }
        return render(request, "accounts/profile.html", context)
    else:
        messages.info(
            request,
            "Your profile information is not available. Please update your profile information.",
        )
        return redirect("index")


@login_required
def delete_account(request):
    if request.method == "POST":
        # Ensure the user confirms deletion by checking the input
        confirmation = request.POST.get("confirmation")
        if confirmation == "حذف":
            # Delete the user's profile
            try:
                profile = Profile.objects.get(user=request.user)
                profile.delete()
            except Profile.DoesNotExist:
                # If the user doesn't have a profile, delete the user directly
                logout(request)  # Log out the user before deletion

                request.user.delete()
                messages.success(request, "Your account has been deleted!")
                return redirect("login")

            # Delete the user
            user = request.user
            logout(request)  # Log out the user before deletion
            user.delete()

            messages.success(request, "Your account has been deleted successfully.")
            return redirect(
                "login"
            )  # Redirect to the home page or another appropriate page

    return redirect("settings")  # Redirect back to settings if not a POST request

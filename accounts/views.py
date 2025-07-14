from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.mail import send_mail
import random
from .forms import CustomUserCreationForm  # Import the custom form
from django.contrib import messages  # Import messages
from geopy.geocoders import Nominatim
from django.conf import settings
from chat.models import FriendRequest
from django.db import models  # For Q objects


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    friend_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    friends = User.objects.filter(
        models.Q(sent_requests__to_user=request.user, sent_requests__status='accepted') |
        models.Q(received_requests__from_user=request.user, received_requests__status='accepted')
    ).distinct()
    if request.method == "POST":
        profile.location = request.POST.get('location', profile.location)
        profile.latitude = request.POST.get('latitude', profile.latitude)
        profile.longitude = request.POST.get('longitude', profile.longitude)
        profile.sports = request.POST.get('sports', profile.sports)
        profile.skill_level = request.POST.get('skill_level', profile.skill_level)
        
        if 'profile_picture' in request.FILES:
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {
        'profile': profile, 
        'user': user,
        'friend_requests': friend_requests,
        'friends': friends,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.location = request.POST.get('location', profile.location)
        profile.sports = request.POST.get('sports', profile.sports)
        profile.skill_level = request.POST.get('skill_level', profile.skill_level)

        if 'profile_picture' in request.FILES:
            if profile.profile_picture:
                profile.profile_picture.delete(save=False)  # ✅ Delete old image to prevent storage issues
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {'profile': profile})





def register(request):
    geolocator = Nominatim(user_agent="sports_matchmaking")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user (this triggers the signal to create a UserProfile)
            user = form.save()

            # Get the UserProfile created by the signal
            profile = user.profile  # Access via the related_name 'profile'

            # Update the profile with form data
            profile.location = form.cleaned_data['location']
            profile.latitude = form.cleaned_data['latitude']
            profile.longitude = form.cleaned_data['longitude']
            profile.sports = form.cleaned_data['sports']
            profile.skill_level = form.cleaned_data['skill_level']

            # Geocode location if coordinates not provided
            if not profile.latitude or not profile.longitude:
                try:
                    location = geolocator.geocode(profile.location)
                    if location:
                        profile.latitude = location.latitude
                        profile.longitude = location.longitude
                except Exception as e:
                    messages.warning(request, "Could not geocode location. Please select it on the map.")

            profile.save()

            # Log the user in and redirect
            login(request, user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('index')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')







    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')
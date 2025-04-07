from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MatchRequest, Notification
from Team.models import Tournament, Team
from .forms import MatchRequestForm, MatchSearchForm
from django.utils import timezone
import requests
from django.contrib import messages

def index(request):
    today = timezone.now().date()
    matches = MatchRequest.objects.filter(date_time__gt=today).order_by('date_time')[:3]
    tournaments = Tournament.objects.all()
    teams = Team.objects.all()
    url = "https://newsapi.org/v2/top-headlines?category=sports&country=us&apiKey=9214f032d62240749fd506e6e6d8c5e0"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])[:5]
    except Exception as e:
        print("Error fetching news:", e)
        articles = []
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at') if request.user.is_authenticated else []
    context = {
        'matches': matches,
        'tournaments': tournaments,
        'teams': teams,
        'notifications': notifications,
        'articles': articles,
    }
    return render(request, 'index.html', context)

# @login_required
# def create_match_request(request):
#     if request.method == 'POST':
#         form = MatchRequestForm(request.POST)
#         if form.is_valid():
#             match = form.save(commit=False)
#             match.user = request.user
#             match.save()
#             Notification.objects.create(
#                 recipient=request.user,
#                 notification_type='match',
#                 related_id=match.id,
#                 message=f"You have successfully created a {match.sport_type} match at {match.location}!"
#             )
#             messages.success(request, "Match request created successfully!")
#             return redirect('match_list')
#     else:
#         form = MatchRequestForm()
#     return render(request, 'matches/create_match.html', {'form': form})

# def match_list(request):
#     today = timezone.now()
#     # Separate upcoming and past matches
#     upcoming_matches = MatchRequest.objects.filter(date_time__gt=today)
#     past_matches = MatchRequest.objects.filter(date_time__lte=today)

#     form = MatchSearchForm(request.GET)
#     if form.is_valid():
#         sport_type = form.cleaned_data.get('sport_type')
#         location = form.cleaned_data.get('location')
#         date = form.cleaned_data.get('date')
#         skill_level = form.cleaned_data.get('skill_level')
#         min_players_needed = form.cleaned_data.get('min_players_needed')
#         if sport_type:
#             upcoming_matches = upcoming_matches.filter(sport_type=sport_type)
#             past_matches = past_matches.filter(sport_type=sport_type)
#         if location:
#             upcoming_matches = upcoming_matches.filter(location__icontains=location)
#             past_matches = past_matches.filter(location__icontains=location)
#         if date:
#             upcoming_matches = upcoming_matches.filter(date_time__date=date)
#             past_matches = past_matches.filter(date_time__date=date)
#         if skill_level:
#             upcoming_matches = upcoming_matches.filter(skill_level=skill_level)
#             past_matches = past_matches.filter(skill_level=skill_level)
#         if min_players_needed is not None:
#             upcoming_matches = upcoming_matches.filter(players_needed__gte=min_players_needed)
#             past_matches = past_matches.filter(players_needed__gte=min_players_needed)

#     return render(request, 'matches/match_list.html', {
#         'upcoming_matches': upcoming_matches,
#         'past_matches': past_matches,
#         'form': form
#     })






from geopy.geocoders import Nominatim
from django.conf import settings


@login_required
def create_match_request(request):
    geolocator = Nominatim(user_agent="sports_matchmaking")
    if request.method == 'POST':
        form = MatchRequestForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.user = request.user
            match.latitude = form.cleaned_data['latitude']
            match.longitude = form.cleaned_data['longitude']

            # Fallback geocoding if coordinates are missing
            if not match.latitude or not match.longitude:
                try:
                    location = geolocator.geocode(match.location)
                    if location:
                        match.latitude = location.latitude
                        match.longitude = location.longitude
                        print(f"Geocoded {match.location} to lat={match.latitude}, lng={match.longitude}")
                    else:
                        print(f"Geocoding failed for {match.location}")
                        messages.warning(request, "Could not geocode location automatically. Using manual location.")
                except Exception as e:
                    print(f"Geocoding error: {e}")
                    messages.warning(request, "Geocoding failed. Using manual location without coordinates.")
            
            match.save()
            Notification.objects.create(
                recipient=request.user,
                notification_type='match',
                related_id=match.id,
                message=f"You have successfully created a {match.sport_type} match at {match.location}!"
            )
            messages.success(request, "Match request created successfully!")
            return redirect('match_list')
    else:
        form = MatchRequestForm()
    return render(request, 'matches/create_match.html', {
        'form': form,
    })
def match_list(request):
    today = timezone.now()
    upcoming_matches = MatchRequest.objects.filter(date_time__gt=today)
    past_matches = MatchRequest.objects.filter(date_time__lte=today)

    form = MatchSearchForm(request.GET)
    if form.is_valid():
        sport_type = form.cleaned_data.get('sport_type')
        location = form.cleaned_data.get('location')
        date = form.cleaned_data.get('date')
        skill_level = form.cleaned_data.get('skill_level')
        min_players_needed = form.cleaned_data.get('min_players_needed')
        if sport_type:
            upcoming_matches = upcoming_matches.filter(sport_type=sport_type)
            past_matches = past_matches.filter(sport_type=sport_type)
        if location:
            upcoming_matches = upcoming_matches.filter(location__icontains=location)
            past_matches = past_matches.filter(location__icontains=location)
        if date:
            upcoming_matches = upcoming_matches.filter(date_time__date=date)
            past_matches = past_matches.filter(date_time__date=date)
        if skill_level:
            upcoming_matches = upcoming_matches.filter(skill_level=skill_level)
            past_matches = past_matches.filter(skill_level=skill_level)
        if min_players_needed is not None:
            upcoming_matches = upcoming_matches.filter(players_needed__gte=min_players_needed)
            past_matches = past_matches.filter(players_needed__gte=min_players_needed)

    match_locations = [
        {'id': m.id, 'lat': m.latitude, 'lng': m.longitude, 'title': f"{m.sport_type} at {m.location}"}
        for m in upcoming_matches if m.latitude and m.longitude
    ]

    return render(request, 'matches/match_list.html', {
        'upcoming_matches': upcoming_matches,
        'past_matches': past_matches,
        'form': form,
        'match_locations': match_locations,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

def match_details(request, match_id):
    match = get_object_or_404(MatchRequest, id=match_id)
    return render(request, 'matches/match_details.html', {'match': match})

@login_required
def accept_match(request, match_id):
    match = get_object_or_404(MatchRequest, id=match_id)
    if request.user == match.user:
        messages.error(request, "You cannot accept your own match!")
    elif request.user in match.accepted_by.all():
        messages.error(request, "You have already accepted this match!")
    elif match.players_remaining() > 0:
        match.accepted_by.add(request.user)
        match.save()
        Notification.objects.create(
            recipient=match.user,
            notification_type='match',
            related_id=match.id,
            message=f"{request.user.username} has joined your {match.sport_type} match at {match.location}!"
        )
        Notification.objects.create(
            recipient=request.user,
            notification_type='match',
            related_id=match.id,
            message=f"You have successfully joined the {match.sport_type} match at {match.location}!"
        )
        messages.success(request, "You have successfully joined the match!")
    else:
        messages.error(request, "This match is already full.")
    return redirect('match_details', match_id=match.id)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if request.method == "POST":
        notification.is_read = True
        notification.save()
    return redirect('index')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if request.method == "POST":
        notification.delete()
        messages.success(request, "Notification deleted successfully!")
    return redirect('index')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'matches/notification.html', {'notifications': user_notifications})

def about_us(request):
    return render(request, 'localsports/about_us.html')

def custom_404(request, exception):
    return render(request, '404.html', {})
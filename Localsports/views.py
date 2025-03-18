

from django.shortcuts import render,redirect
from .models import Match,MatchRequest,MatchNotification
from django.contrib.auth.decorators import login_required
from .forms import MatchRequestForm
from django.utils import timezone

# from .forms import RegistrationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import MatchRequestForm, MatchSearchForm
from Team.models import Tournament, Team  # Import from Team app
import requests




def index(request):
    today = timezone.now().date()
    matches = MatchRequest.objects.filter(date_time__gt=today).order_by('date_time')[:3]  # Limit to 3
    
    # Fetch all tournaments and teams
    tournaments = Tournament.objects.all()
    teams = Team.objects.all()
    url = "https://newsapi.org/v2/top-headlines?category=sports&country=us&apiKey=9214f032d62240749fd506e6e6d8c5e0"
    try:
        response = requests.get(url)
        data = response.json()

        # Extract only relevant articles
        articles = data.get("articles", [])[:5]  # Get the top 5 recent sports news

    except Exception as e:
        print("Error fetching news:", e)
        articles = []

    notifications = MatchNotification.objects.filter(recipient=request.user, is_read=False) if request.user.is_authenticated else []

    context = {
        'matches': matches,
        'tournaments': tournaments,
        'teams': teams,
        'notifications': notifications,
        'articles': articles,
    }
    return render(request, 'index.html', context)





def custom_404(request, exception):
    return render(request, '404.html',{})


@login_required
def create_match_request(request):
    if request.method == 'POST':
        form = MatchRequestForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.user = request.user
            match.save()
            messages.success(request, "Match request created successfully!")
            return redirect('match_list')
    else:
        form = MatchRequestForm()
    return render(request, 'matches/create_match.html', {'form': form})


def match_list(request):
    # matches = MatchRequest.objects.filter(accepted_by__isnull=True)
    matches = MatchRequest.objects.all()

    form = MatchSearchForm(request.GET)

    if form.is_valid():
        sport_type = form.cleaned_data.get('sport_type')
        location = form.cleaned_data.get('location')
        date = form.cleaned_data.get('date')
        skill_level = form.cleaned_data.get('skill_level')
        min_players_needed = form.cleaned_data.get('min_players_needed')

        if sport_type:
            matches = matches.filter(sport_type=sport_type)
        if location:
            matches = matches.filter(location__icontains=location)  # Partial match for location
        if date:
            matches = matches.filter(date_time__date=date)
        if skill_level:
            matches = matches.filter(skill_level=skill_level)
        if min_players_needed is not None:
            matches = matches.filter(players_needed__gte=min_players_needed)

    return render(request, 'matches/match_list.html', {'matches': matches,'form': form})


def match_details(request, match_id):
    match = get_object_or_404(MatchRequest, id=match_id)
    return render(request, 'matches/match_details.html', {'match': match})


@login_required
def accept_match(request, match_id):
    match = get_object_or_404(MatchRequest, id=match_id)

    if request.user in match.accepted_by.all():
        messages.error(request, "You have already joined this match!")
    elif match.players_remaining() > 0:
        match.accepted_by.add(request.user)  # ✅ Fix: Add user to ManyToMany field
        match.save()

        # Create a notification for the match creator
        MatchNotification.objects.create(
            recipient=match.user,
            match=match,
            message=f"{request.user.username} has joined your {match.sport_type} match at {match.location}!"
        )

        messages.success(request, "You have successfully joined the match!")
    else:
        messages.error(request, "This match is already full.")

    return redirect('match_details', match_id=match.id) 


# @login_required
# def accept_match(request, match_id):
#     match = get_object_or_404(MatchRequest, id=match_id)

#     if request.user in match.accepted_by.all():
#         messages.error(request, "You have already joined this match!")
#     elif match.players_remaining() > 0:
#         match.accepted_by.add(request.user)  # ✅ Add user to match
#         match.save()

#         # Create a notification for the match creator
#         MatchNotification.objects.create(
#             recipient=match.user,
#             match=match,
#             message=f"{request.user.username} has joined your {match.sport_type} match at {match.location}!"
#         )

#         messages.success(request, "You have successfully joined the match!")
#     else:
#         messages.error(request, "This match is already full.")

#     return redirect('match_list')

@login_required
def notifications(request):
    user_notifications = MatchNotification.objects.filter(recipient=request.user, is_read=False)
    for notification in user_notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'matches/notification.html', {'notifications': user_notifications})

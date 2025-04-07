from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, Tournament
from .forms import TeamCreateForm, TeamUpdateForm, TeamFilterForm, TournamentForm, JoinTournamentForm
from Localsports.models import Notification
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import requests
from geopy.geocoders import Nominatim

# @login_required
# def create_team(request):
#     if request.method == 'POST':
#         form = TeamCreateForm(request.POST)
#         if form.is_valid():
#             team = form.save(commit=False)
#             team.captain = request.user
#             team.save()
#             team.players.add(request.user)
#             messages.success(request, "Team created successfully!")
#             return redirect('team_list')
#     else:
#         form = TeamCreateForm()
#     return render(request, 'teams/create_team.html', {'form': form})
from geopy.geocoders import Nominatim
from django.conf import settings

@login_required
def create_team(request):
    geolocator = Nominatim(user_agent="sports_matchmaking")
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.captain = request.user
            team.latitude = form.cleaned_data['latitude']
            team.longitude = form.cleaned_data['longitude']
            if not team.latitude or not team.longitude:
                try:
                    location = geolocator.geocode(team.location)
                    if location:
                        team.latitude = location.latitude
                        team.longitude = location.longitude
                        print(f"Geocoded {team.location} to lat={team.latitude}, lng={team.longitude}")
                    else:
                        print(f"Geocoding failed for {team.location}")
                        messages.warning(request, "Could not geocode location automatically. Using manual location.")
                except Exception as e:
                    print(f"Geocoding error: {e}")
                    messages.warning(request, "Geocoding failed. Using manual location without coordinates.")
            team.save()
            team.players.add(request.user)
            messages.success(request, "Team created successfully!")
            return redirect('team_list')
    else:
        form = TeamCreateForm()
    return render(request, 'teams/create_team.html', {'form': form})


def team_list(request):
    teams = Team.objects.all()
    form = TeamFilterForm(request.GET)
    if form.is_valid():
        sport_type = form.cleaned_data.get('sport_type')
        skill_level = form.cleaned_data.get('skill_level')
        location = form.cleaned_data.get('location')
        if sport_type:
            teams = teams.filter(sport_type=sport_type)
        if skill_level:
            teams = teams.filter(skill_level=skill_level)
        if location:
            teams = teams.filter(location__icontains=location)
    return render(request, 'teams/team_list.html', {'teams': teams, "form": form})

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user in team.players.all():
        messages.error(request, "You are already a member of this team!")
        Notification.objects.create(
            recipient=request.user,
            notification_type='team',
            related_id=team.id,
            message=f"You are already a member of the team: {team.name}"
        )
    else:
        team.players.add(request.user)
        Notification.objects.create(
            recipient=request.user,
            notification_type='team',
            related_id=team.id,
            message=f"You have successfully joined the team: {team.name}"
        )
        if team.captain:
            Notification.objects.create(
                recipient=team.captain,
                notification_type='team',
                related_id=team.id,
                message=f"{request.user.username} has joined your team: {team.name}"
            )
        messages.success(request, "You have successfully joined the team!")
    return redirect('team_list')

@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user in team.players.all():
        team.players.remove(request.user)
        messages.success(request, f"You left the team: {team.name}")
    else:
        messages.error(request, "You are not part of this team.")
    return redirect('team_list')

@login_required
def manage_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if team.captain != request.user:
        messages.error(request, "You are not the team captain.")
        return redirect('team_list')
    if request.method == 'POST':
        form = TeamUpdateForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully!")
            return redirect('team_list')
    else:
        form = TeamUpdateForm(instance=team)
    return render(request, 'teams/manage_team.html', {'form': form, 'team': team})

# @login_required
# def create_tournament(request):
#     if request.method == "POST":
#         form = TournamentForm(request.POST)
#         if form.is_valid():
#             tournament = form.save(commit=False)
#             tournament.created_by = request.user
#             tournament.save()
#             # Send email to creator
#             subject = f"New Tournament Created: {tournament.name}"
#             message = (
#                 f"Dear {request.user.username},\n\n"
#                 f"You have successfully created a new tournament:\n"
#                 f"Name: {tournament.name}\n"
#                 f"Sport Type: {tournament.sport_type}\n"
#                 f"Location: {tournament.location}\n"
#                 f"Start Date: {tournament.start_date}\n"
#                 f"End Date: {tournament.end_date}\n"
#                 f"Required Team Size: {tournament.required_team_size}\n\n"
#                 f"Thank you for organizing this event!"
#             )
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [request.user.email],
#                 fail_silently=False,
#             )
#             messages.success(request, "Tournament created successfully!")
#             return redirect('tournament_list')
#     else:
#         form = TournamentForm()
#     return render(request, "tournaments/create_tournament.html", {"form": form})

@login_required
def create_tournament(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.latitude = request.POST.get('latitude', None)
            tournament.longitude = request.POST.get('longitude', None)
            if not tournament.latitude or not tournament.longitude:
                try:
                    geolocator = Nominatim(user_agent="sports_matchmaking")
                    location = geolocator.geocode(tournament.location)
                    if location:
                        tournament.latitude = location.latitude
                        tournament.longitude = location.longitude
                        print(f"Geocoded {tournament.location} to lat={tournament.latitude}, lng={tournament.longitude}")
                    else:
                        print(f"Geocoding failed for {tournament.location}")
                        messages.warning(request, "Could not geocode location automatically. Using manual location.")
                except Exception as e:
                    print(f"Geocoding error: {e}")
                    messages.warning(request, "Geocoding failed. Using manual location without coordinates.")
            tournament.save()
            # Send email to creator
            subject = f"New Tournament Created: {tournament.name}"
            message = (
                f"Dear {request.user.username},\n\n"
                f"You have successfully created a new tournament:\n"
                f"Name: {tournament.name}\n"
                f"Sport Type: {tournament.sport_type}\n"
                f"Location: {tournament.location}\n"
                f"Start Date: {tournament.start_date}\n"
                f"End Date: {tournament.end_date}\n"
                f"Required Team Size: {tournament.required_team_size}\n\n"
                f"Thank you for organizing this event!"
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, "Tournament created successfully!")
            return redirect('tournament_list')
    else:
        form = TournamentForm()
    return render(request, "tournaments/create_tournament.html", {"form": form})



@login_required
def join_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    user_team = Team.objects.filter(captain=request.user).first()
    
    if not user_team:
        messages.error(request, "You must be a team captain to register for a tournament.")
        return render(request, 'tournaments/join_tournament.html', {'tournament': tournament})

    if user_team in tournament.teams.all():
        messages.error(request, "Your team is already registered for this tournament!")
        return render(request, 'tournaments/join_tournament.html', {'tournament': tournament})

    if request.method == "POST":
        form = JoinTournamentForm(request.POST)
        if form.is_valid():
            team_size = form.cleaned_data['team_size']
            if team_size == tournament.required_team_size:
                tournament.teams.add(user_team)
                Notification.objects.create(
                    recipient=request.user,
                    notification_type='tournament',
                    related_id=tournament.id,
                    message=f"Your team {user_team.name} has been registered for the tournament: {tournament.name}"
                )
                if tournament.created_by:
                    Notification.objects.create(
                        recipient=tournament.created_by,
                        notification_type='tournament',
                        related_id=tournament.id,
                        message=f"Team {user_team.name} has registered for your tournament: {tournament.name}"
                    )
                # Send email to user
                subject = f"Joined Tournament: {tournament.name}"
                message = (
                    f"Dear {request.user.username},\n\n"
                    f"Your team {user_team.name} has successfully joined the tournament:\n"
                    f"Name: {tournament.name}\n"
                    f"Sport Type: {tournament.sport_type}\n"
                    f"Location: {tournament.location}\n"
                    f"Start Date: {tournament.start_date}\n"
                    f"End Date: {tournament.end_date}\n"
                    f"Required Team Size: {tournament.required_team_size}\n\n"
                    f"Get ready for the event!"
                )
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
                messages.success(request, "Your team has been registered for the tournament!")
                return redirect('tournament_detail', tournament_id=tournament.id)
            else:
                messages.error(request, f"Your team size ({team_size}) does not match the required size ({tournament.required_team_size}) for {tournament.sport_type}.")
    else:
        form = JoinTournamentForm()

    return render(request, 'tournaments/join_tournament.html', {'form': form, 'tournament': tournament})
def tournament_list(request):
    current_date = timezone.now().date()  # Current date: April 07, 2025
    tournaments = Tournament.objects.all().order_by('start_date')
    
    # Separate current and past tournaments
    current_tournaments = tournaments.filter(end_date__gte=current_date)
    past_tournaments = tournaments.filter(end_date__lt=current_date)

    return render(request, "tournaments/tournament_list.html", {
        "current_tournaments": current_tournaments,
        "past_tournaments": past_tournaments
    })
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    return render(request, "tournaments/tournament_detail.html", {"tournament": tournament})

@login_required
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if request.user == tournament.created_by:
        tournament.delete()
        messages.success(request, "Tournament deleted successfully!")
        return redirect('tournament_list')
    else:
        messages.error(request, "You are not allowed to delete this tournament.")
        return redirect('tournament_detail', tournament_id=tournament.id)
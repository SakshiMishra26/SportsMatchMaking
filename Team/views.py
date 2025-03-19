from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, Tournament
from .forms import TeamCreateForm, TeamUpdateForm, TeamFilterForm, TournamentForm
from Localsports.models import Notification  # Import the new Notification model

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.captain = request.user
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
        # Create a notification for the user
        Notification.objects.create(
            recipient=request.user,
            notification_type='team',
            related_id=team.id,
            message=f"You are already a member of the team: {team.name}"
        )
    else:
        team.players.add(request.user)
        # Create a notification for the user
        Notification.objects.create(
            recipient=request.user,
            notification_type='team',
            related_id=team.id,
            message=f"You have successfully joined the team: {team.name}"
        )
        # Create a notification for the team captain
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

@login_required
def create_tournament(request):
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.save()
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
        # Create a notification for the user
        Notification.objects.create(
            recipient=request.user,
            notification_type='tournament',
            related_id=tournament.id,
            message="You must be a team captain to register for a tournament."
        )
        return redirect('tournament_detail', tournament_id=tournament.id)
    if user_team in tournament.teams.all():
        messages.error(request, "Your team is already registered for this tournament!")
        # Create a notification for the user
        Notification.objects.create(
            recipient=request.user,
            notification_type='tournament',
            related_id=tournament.id,
            message=f"Your team {user_team.name} is already registered for the tournament: {tournament.name}"
        )
    else:
        tournament.teams.add(user_team)
        # Create a notification for the user
        Notification.objects.create(
            recipient=request.user,
            notification_type='tournament',
            related_id=tournament.id,
            message=f"Your team {user_team.name} has been registered for the tournament: {tournament.name}"
        )
        # Create a notification for the tournament creator (if applicable)
        if tournament.created_by:
            Notification.objects.create(
                recipient=tournament.created_by,
                notification_type='tournament',
                related_id=tournament.id,
                message=f"Team {user_team.name} has registered for your tournament: {tournament.name}"
            )
        messages.success(request, "Your team has been registered for the tournament!")
    return redirect('tournament_detail', tournament_id=tournament.id)

def tournament_list(request):
    tournaments = Tournament.objects.all().order_by('start_date')
    return render(request, "tournaments/tournament_list.html", {"tournaments": tournaments})

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
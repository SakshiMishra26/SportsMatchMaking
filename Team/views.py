from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team,Tournament
from .forms import TeamCreateForm, TeamUpdateForm,TeamFilterForm,TournamentForm

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.captain = request.user  # ✅ Set the logged-in user as captain
            team.save()
            team.players.add(request.user)  # ✅ Captain automatically joins the team
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
    return render(request, 'teams/team_list.html', {'teams': teams,"form": form})

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.players.all():
        team.players.add(request.user)
        messages.success(request, f"You joined the team: {team.name}")
    else:
        messages.error(request, "You are already in this team.")
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

# @login_required
# def join_tournament(request, tournament_id):
#     tournament = get_object_or_404(Tournament, id=tournament_id)
#     user_team = Team.objects.filter(players=request.user).first()

#     if user_team and user_team not in tournament.teams.all():
#         tournament.teams.add(user_team)
    
#     return redirect('tournament_list')

@login_required
def join_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    user_team = Team.objects.filter(captain=request.user).first()  # ✅ Only fetch user's captain team

    if not user_team:
        messages.error(request, "You must be a team captain to register for a tournament.")
        return redirect('tournament_detail', tournament_id=tournament.id)

    if user_team in tournament.teams.all():
        messages.warning(request, "Your team is already registered for this tournament.")
    else:
        tournament.teams.add(user_team)
        messages.success(request, "Your team has been registered successfully!")

    return redirect('tournament_detail', tournament_id=tournament.id)

def tournament_list(request):
    tournaments = Tournament.objects.all()
    return render(request, "tournaments/tournament_list.html", {"tournaments": tournaments})


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    return render(request, "tournaments/tournament_detail.html", {"tournament": tournament})


@login_required
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.user == tournament.created_by:  # ✅ Only allow creator to delete
        tournament.delete()
        messages.success(request, "Tournament deleted successfully!")
        return redirect('tournament_list')
    else:
        messages.error(request, "You are not allowed to delete this tournament.")
        return redirect('tournament_detail', tournament_id=tournament.id)
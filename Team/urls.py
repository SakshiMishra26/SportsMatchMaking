from django.urls import path
from .views import create_team, team_list, join_team, leave_team, manage_team,create_tournament, tournament_list, join_tournament,tournament_detail,delete_tournament

urlpatterns = [
    path('teams/', team_list, name='team_list'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/join/<int:team_id>/', join_team, name='join_team'),
    path('teams/leave/<int:team_id>/', leave_team, name='leave_team'),
    path('teams/manage/<int:team_id>/', manage_team, name='manage_team'),
     path('tournaments/', tournament_list, name='tournament_list'),
    path('tournaments/create/', create_tournament, name='create_tournament'),
    path('tournaments/join/<int:tournament_id>/', join_tournament, name='join_tournament'),
    path('tournaments/<int:tournament_id>/', tournament_detail, name='tournament_detail'),
        path('tournaments/delete/<int:tournament_id>/', delete_tournament, name='delete_tournament'),


]

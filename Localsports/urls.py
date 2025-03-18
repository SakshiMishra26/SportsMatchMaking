from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    

    # path('match/request/<int:match_id>/', views.create_match_request, name='create_match_request'),
    path('match/request/', views.create_match_request, name='create_match_request'),  
# path('match/accept/<int:match_id>/', views.accept_match, name='accept_match'),
    # path('request/', views.request_match, name='request_match'),
    # path('match-requests/', views.match_requests, name='match_requests'),
    path('matches/', views.match_list, name='match_list'),
        path('matches/<int:match_id>/', views.match_details, name='match_details'),

    path('matches/accept/<int:match_id>/', views.accept_match, name='accept_match'),
    path('notifications/', views.notifications, name='notifications'),
]


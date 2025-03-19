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
    path('about-us/', views.about_us, name='about_us'),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),  # New URL
]


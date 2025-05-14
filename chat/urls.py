from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('manage_friend_requests/', views.manage_friend_requests, name='manage_friend_requests'),
    path('respond_friend_request/<int:request_id>/', views.respond_friend_request, name='respond_friend_request'),
    path('send_message/', views.send_message, name='send_message'),
    path('messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('friends/', views.friends_list, name='friends_list'),
]
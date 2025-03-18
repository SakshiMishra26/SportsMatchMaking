from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('accounts/profile/', views.profile, name='profile_default'),
# path('accounts/<str:username>/', views.profile, name='profile'),

     path('signup/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
        # path('send_otp/', views.send_otp, name='send_otp'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
 

]
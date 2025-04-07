from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    location = forms.CharField(max_length=100, required=True)
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    sports = forms.CharField(max_length=100, required=True)
    skill_level = forms.ChoiceField(choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ], required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'location', 'latitude', 'longitude', 'sports', 'skill_level']
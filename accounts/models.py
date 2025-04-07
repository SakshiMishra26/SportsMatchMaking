from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # ✅ Changed from 'accounts_profile' to 'profile'
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)  # New field
    longitude = models.FloatField(null=True, blank=True)
    sports = models.CharField(max_length=100, blank=True)
    skill_level = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ], blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # ✅ New profile image field


    def __str__(self):
        return self.user.username

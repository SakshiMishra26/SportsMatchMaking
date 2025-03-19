from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    SPORT_CHOICES = [
        ('Football', 'Football'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Badminton', 'Badminton'),
        ('Cricket', 'Cricket'),
    ]
    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    name = models.CharField(max_length=100, unique=True)
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    skill_level = models.CharField(max_length=50, choices=SKILL_LEVEL_CHOICES, default='Beginner')
    location = models.CharField(max_length=100, default="Unknown")
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name="captained_teams")
    players = models.ManyToManyField(User, related_name="teams", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_captain(self, user):
        return self.captain == user

    def __str__(self):
        return f"{self.name} ({self.sport_type})"


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=50, choices=[
        ('Football', 'Football'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Cricket', 'Cricket'),
    ])
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  # New field
    teams = models.ManyToManyField(Team, related_name="tournaments", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tournaments")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.sport_type}"
    

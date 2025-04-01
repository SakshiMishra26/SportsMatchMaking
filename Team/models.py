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
    SPORT_CHOICES = [
        ('Football', 'Football'),
        ('Basketball', 'Basketball'),
        ('Tennis', 'Tennis'),
        ('Cricket', 'Cricket'),
    ]
    # Define required team sizes for each sport
    SPORT_TEAM_SIZES = {
        'Football': 11,  # 11 players per team
        'Basketball': 5,  # 5 players per team
        'Tennis': 2,     # Doubles (can be 1 for singles, but we'll assume doubles)
        'Cricket': 11,   # 11 players per team
    }
    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team, related_name="tournaments", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tournaments")
    is_active = models.BooleanField(default=True)
    # required_team_size = models.IntegerField(editable=False)
    required_team_size = models.IntegerField(default=0)  # Temporary default for migrations

    def save(self, *args, **kwargs):
        # Ensure required_team_size is set based on sport_type
        self.required_team_size = self.SPORT_TEAM_SIZES.get(self.sport_type, 0)
        super().save(*args, **kwargs)

    def can_team_join(self, team):
        # Check if team meets size and sport requirements
        return (team.sport_type == self.sport_type and
                team.players.count() == self.required_team_size)

    def __str__(self):
        return f"{self.name} - {self.sport_type}"
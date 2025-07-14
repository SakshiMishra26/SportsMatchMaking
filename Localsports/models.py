from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile





class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

 
class Match(models.Model):
    title = models.CharField(max_length=200,null=True, blank=True)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    category = models.CharField(max_length=100, choices=[('football', 'Football'), ('basketball', 'Basketball')],default='football')
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_matches',null=True, blank=True)
    requested_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='requested_matches', null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.title




class MatchRequest(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_requests")
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES,default='Football')
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)  # New field
    longitude = models.FloatField(null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES,default='Beginner')
    players_needed = models.PositiveIntegerField(default=2)
    accepted_by = models.ManyToManyField(User, related_name="joined_matches", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches", null=True, blank=True)


    # accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_matches")
    created_at = models.DateTimeField(auto_now_add=True)

    def players_remaining(self):
        # return self.players_needed - self.accepted_by.count()
        return max(0, self.players_needed - self.accepted_by.count())


    def __str__(self):
        return f"{self.sport_type} match at {self.location} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('match', 'Match'),
        ('team', 'Team'),
        ('tournament', 'Tournament'),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    related_id = models.PositiveIntegerField()  # ID of the related object (match, team, or tournament)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"
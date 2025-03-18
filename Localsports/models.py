from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     location = models.CharField(max_length=100, blank=True)
#     sports = models.CharField(max_length=100, blank=True)
#     skill_level = models.CharField(max_length=50, choices=[
#         ('Beginner', 'Beginner'),
#         ('Intermediate', 'Intermediate'),
#         ('Advanced', 'Advanced'),
#     ], blank=True)

#     def __str__(self):
#         return self.user.username



#THis is new 
# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     match_category = models.CharField(max_length=100, choices=[('football', 'Football'), ('basketball', 'Basketball')])
#     team_members = models.TextField(blank=True)  # Comma-separated names of teammates
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="customuser_groups",  # Unique related_name to avoid conflict
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="customuser_permissions",  # Unique related_name to avoid conflict
#         blank=True
#     )
#     def __str__(self):
#         return self.username


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     sports = models.ManyToManyField('Sport')
#     location = models.CharField(max_length=255)
#     skill_level = models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])

#     def __str__(self):
#         return self.user.username

class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Match(models.Model):
#     sport = models.ForeignKey(Sport, on_delete=models.CASCADE,default=1)
#     players = models.ManyToManyField(UserProfile)
#     date = models.DateTimeField()
#     location = models.CharField(max_length=255,default='Pune')

#     def __str__(self):
#         return f"{self.sport.name} - {self.date}"
    
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


# class MatchRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the request
#     location = models.CharField(max_length=255)  # Location of the match
#     date = models.DateField()  # Date of the match
#     time = models.TimeField()  # Time of the match
#     team_size = models.IntegerField()  # Size of the team requested
#     created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the request was made

#     def __str__(self):
#         return f"Match request by {self.user.username} on {self.date} at {self.time}"
    



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

class MatchNotification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    match = models.ForeignKey(MatchRequest, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"

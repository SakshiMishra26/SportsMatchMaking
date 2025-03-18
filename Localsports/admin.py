from django.contrib import admin
from .models import Match,MatchRequest,UserProfile

# Register your models here.
admin.site.register(Match)
admin.site.register(MatchRequest)
# admin.site.register(UserProfile)


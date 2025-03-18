from django import forms
from django.contrib.auth.models import User

from .models import MatchRequest


from django import forms
from .models import MatchRequest

class MatchSearchForm(forms.Form):
    sport_type = forms.ChoiceField(choices=[('', 'All Sports')] + MatchRequest.SPORT_CHOICES, required=False)
    location = forms.CharField(max_length=100, required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    skill_level = forms.ChoiceField(choices=[('', 'Any Skill Level')] + MatchRequest.SKILL_LEVEL_CHOICES, required=False)
    min_players_needed = forms.IntegerField(required=False, min_value=1, label="Min Players Needed")


class MatchRequestForm(forms.ModelForm):
    class Meta:
        model = MatchRequest
        fields = ['sport_type', 'location', 'date_time', 'skill_level','players_needed']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

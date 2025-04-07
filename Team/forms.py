from django import forms
from .models import Team, Tournament


class TeamCreateForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Team
        fields = ['name', 'sport_type', 'skill_level', 'location', 'latitude', 'longitude']

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'sport_type']

class TeamFilterForm(forms.Form):
    sport_type = forms.ChoiceField(choices=[('', 'All Sports')] + Team.SPORT_CHOICES, required=False)
    skill_level = forms.ChoiceField(choices=[('', 'All Skill Levels')] + Team.SKILL_LEVEL_CHOICES, required=False)
    location = forms.CharField(max_length=100, required=False)

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'sport_type', 'location', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class JoinTournamentForm(forms.Form):
    team_size = forms.IntegerField(min_value=1, label="Your Team Size", help_text="Enter the number of players in your team.")
from django import forms
from .models import Team
from .models import Tournament


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'sport_type','skill_level', 'location']

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
        fields = ['name', 'sport_type', 'location', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # ✅ HTML5 datetime picker
        }
        

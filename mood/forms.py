from django import forms
from .models import Mood

class MoodForm(forms.ModelForm):

    class Meta:
        model = Mood
        fields = ['mood','note']


CHOICES = [
    (0, "Never"),
    (1, "Rarely"),
    (2, "Sometimes"),
    (3, "Often"),
]


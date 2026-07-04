from django import forms
from .models import Profile
class AssessmentForm(forms.Form):
    q1 = forms.ChoiceField(
        label="I feel nervous or anxious",
        choices=[(0,"Not at all"),(1,"Several days"),(2,"More than half the days"),(3,"Nearly every day")]
    )

    q2 = forms.ChoiceField(
        label="I have trouble sleeping",
        choices=[(0,"Not at all"),(1,"Several days"),(2,"More than half the days"),(3,"Nearly every day")]
    )

    q3 = forms.ChoiceField(
        label="I feel tired or have little energy",
        choices=[(0,"Not at all"),(1,"Several days"),(2,"More than half the days"),(3,"Nearly every day")]
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'concern']    
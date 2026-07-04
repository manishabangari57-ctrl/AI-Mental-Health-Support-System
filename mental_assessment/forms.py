from django import forms

CHOICES = [
    (0, "Never"),
    (1, "Rarely"),
    (2, "Sometimes"),
    (3, "Often"),
]

class AssessmentForm(forms.Form):

    q1 = forms.ChoiceField(label="I feel stressed", choices=CHOICES, widget=forms.RadioSelect)
    q2 = forms.ChoiceField(label="I feel anxious", choices=CHOICES, widget=forms.RadioSelect)
    q3 = forms.ChoiceField(label="I feel overwhelmed", choices=CHOICES, widget=forms.RadioSelect)
    q4 = forms.ChoiceField(label="I struggle to relax", choices=CHOICES, widget=forms.RadioSelect)
    q5 = forms.ChoiceField(label="I feel mentally exhausted", choices=CHOICES, widget=forms.RadioSelect)
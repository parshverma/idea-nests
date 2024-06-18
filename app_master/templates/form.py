# forms.py

from django import forms
from .models import Feedback

class feedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'details', 'town']

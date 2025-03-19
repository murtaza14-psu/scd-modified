from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a message...'}),
        required=False
    )

    class Meta:
        model = Application
        fields = ['message']

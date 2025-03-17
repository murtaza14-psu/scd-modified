from django import forms
from .models import Opportunity

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'description', 'location', 'date', 'required_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control'}),
        }

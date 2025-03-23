from django import forms
from django.core.validators import RegexValidator
from .models import Application

class ApplicationForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a message...'}),
        required=False
    )

    class Meta:
        model = Application
        fields = ['message']

class AttendanceForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(
        choices=[
            ('checked_in', 'Checked In'),
            ('completed', 'Completed'),
            ('no_show', 'No Show')
        ],
        widget=forms.Select
    )

class AttendanceCheckoutForm(forms.Form):
    hours_contributed = forms.CharField(
        label='Hours Contributed',
        validators=[RegexValidator(regex=r'^\d+(\.\d{1,2})?$', message='Enter a valid number.')],
        required=True
    )
    notes = forms.CharField(widget=forms.Textarea, required=False)

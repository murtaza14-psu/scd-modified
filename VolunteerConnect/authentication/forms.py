from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}),
        initial='volunteer'
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    org_name = forms.CharField(
        required=False,  # Optional for volunteers
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_organization_name'})
    )
    org_description = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'id_description', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'role', 'org_name', 'org_description']

    def clean_email(self):
        """ Ensure email is unique """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_name(self):
        """ Ensure name contains only alphabets and spaces """
        name = self.cleaned_data.get("name")
        if not name.replace(" ", "").isalpha():
            raise ValidationError("Name should only contain letters and spaces.")
        return name

    def clean(self):
        """ Custom validation for NGO role fields """
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        org_name = cleaned_data.get("org_name")

        if role == "ngo" and not org_name:
            self.add_error("org_name", "Organization name is required for NGO role.")

        return cleaned_data

    def save(self, commit=True):
        """Override save() to auto-generate a username and create NGOProfile if applicable"""
        user = super().save(commit=False)
        user.username = user.email.split('@')[0]  # Generate username from email

        if commit:
            user.save()

            # Automatically create NGOProfile if role is 'ngo'
            if user.role == "ngo":
                NGOProfile.objects.create(
                    user=user,
                    organization_name=self.cleaned_data["org_name"],
                    description=self.cleaned_data["org_description"]
                )

            elif user.role == "volunteer":
                VolunteerProfile.objects.create(user=user)  # Create VolunteerProfile

        return user

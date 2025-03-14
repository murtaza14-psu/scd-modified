from django.contrib.auth.models import AbstractUser
from django.db import models

# superuser:syedmhussain201@gmail.com
# password: admin

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('ngo', 'NGO'),
    )

    email = models.EmailField(unique=True)  # Ensure email is unique for login
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='volunteer')
    org_name = models.CharField(max_length=255, blank=True, null=True)
    org_description = models.TextField(blank=True, null=True)

    username = models.CharField(max_length=150, blank=True, null=True)  # Allow duplicate usernames
    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['username', 'user_type']  # Required when creating a user via CLI

    def __str__(self):
        return self.email  # Changed to email since username is non-unique

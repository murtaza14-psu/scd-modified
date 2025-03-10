from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('volunteer', 'Volunteer'),
        ('ngo', 'NGO'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='volunteer')  # Set a default
    org_name = models.CharField(max_length=255, blank=True, null=True)
    org_description = models.TextField(blank=True, null=True)

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','user_type']  # Ensure user_type is required

    def __str__(self):
        return self.email

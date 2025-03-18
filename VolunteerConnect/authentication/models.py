from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, email, username, name, password=None, role='volunteer'):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(email=self.normalize_email(email), username=username, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)

        if role == 'ngo':
            NGOProfile.objects.create(user=user)

        return user
    
    def create_superuser(self, email, username, name, password):
        user = self.create_user(email, username, name, password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('ngo', 'NGO'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(default=now)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django Admin
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'  # Email remains the primary identifier
    REQUIRED_FIELDS = ['username', 'name']  # Make sure username is required during superuser creation
    
    def __str__(self):
        return self.email


class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
    skills = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.name

class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ngo_profile')
    organization_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_ngos')


#logic for if admin changes the status to rejected then the opportunities of the logged in 
#ngos are deleted
    def save(self, *args, **kwargs):
        # Check if the verification_status changed to 'rejected'
        if self.pk:  # Ensure this is not a new instance
            previous_status = NGOProfile.objects.get(pk=self.pk).verification_status
            if previous_status != "rejected" and self.verification_status == "rejected":
                self.delete_opportunities()

        super().save(*args, **kwargs)

    def delete_opportunities(self):
        """Delete all opportunities created by this NGO when rejected."""
        from opportunities.models import Opportunity  # Import inside function to avoid circular import
        Opportunity.objects.filter(ngo=self).delete()
    
    def __str__(self):
        return self.organization_name

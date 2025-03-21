from django.db import models
from django.utils.timezone import now
from authentication.models import VolunteerProfile
from opportunities.models import Opportunity

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.volunteer.user.username} - {self.opportunity.title} ({self.status})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('checked_in', 'Checked In'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    ]

    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='attendances')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='checked_in')
    check_in_time = models.DateTimeField(default=now, blank=True, null=True)
    check_out_time = models.DateTimeField(blank=True, null=True)
    hours_contributed = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.volunteer.user.username} - {self.opportunity.title} ({self.status})"

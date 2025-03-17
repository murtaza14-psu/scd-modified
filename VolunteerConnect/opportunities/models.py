from django.db import models
from django.utils.timezone import now
from authentication.models import NGOProfile

class Opportunity(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('removed', 'Removed'),
    ]

    CONTENT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('flagged', 'Flagged'),
        ('removed', 'Removed'),
    ]

    ngo = models.ForeignKey(NGOProfile, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    required_skills = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    content_status = models.CharField(max_length=20, choices=CONTENT_STATUS_CHOICES, default='active')
    moderation_reason = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

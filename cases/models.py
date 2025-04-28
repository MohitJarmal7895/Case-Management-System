import datetime
import uuid
from django.db import models
from django.conf import settings
from clients.models import Client

class Case(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    case_number = models.IntegerField()
    assigned_attorney = models.CharField(max_length=50)
    description = models.TextField(default=" ")
    court_name = models.CharField(max_length=50,default='District Court')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    filing_date = models.DateField(default=datetime.date.today)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EmailNotification(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50)
    recipient = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('QUEUED', 'Queued'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('OPENED', 'Opened'),
        ('CLICKED', 'Clicked')
    ], default='QUEUED')
    tracking_id = models.UUIDField(unique=True, default=uuid.uuid4)
    error_message = models.TextField(blank=True, null=True)

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    notification_types = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'

    def __str__(self):
        return f"Preferences for {self.user.email}"

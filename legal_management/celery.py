import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_management.settings')

app = Celery('legal_management')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure Celery Beat schedule
app.conf.beat_schedule = {
    'daily-appointment-reminders': {
        'task': 'appointments.tasks.send_daily_appointment_reminders',
        'schedule': 3600.0 * 24,  # Run daily
        'options': {'queue': 'default'},
    },
    'cleanup-old-appointments': {
        'task': 'appointments.tasks.cleanup_past_appointments',
        'schedule': 3600.0 * 24 * 7,  # Run weekly
        'options': {'queue': 'default'},
    },
}

app.conf.timezone = settings.TIME_ZONE
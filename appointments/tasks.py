from celery import shared_task
from django.utils import timezone
from .models import Appointment
from .utils import send_appointment_notification

@shared_task
def send_daily_appointment_reminders():
    """Send reminders for appointments scheduled for tomorrow"""
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    upcoming_appointments = Appointment.objects.filter(
        date_time__date=tomorrow.date(),
        status='SCHEDULED'
    )

    for appointment in upcoming_appointments:
        send_appointment_notification(appointment, 'reminder')
    
    return f"Sent reminders for {upcoming_appointments.count()} appointments"

@shared_task
def send_immediate_reminder(appointment_id):
    """Send an immediate reminder for a specific appointment"""
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        send_appointment_notification(appointment, 'reminder')
        return f"Sent reminder for appointment: {appointment.title}"
    except Appointment.DoesNotExist:
        return "Appointment not found"

@shared_task
def cleanup_past_appointments():
    """Archive appointments older than 6 months"""
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    old_appointments = Appointment.objects.filter(
        date_time__lt=six_months_ago,
        status='COMPLETED'
    )
    
    count = old_appointments.update(is_archived=True)
    return f"Archived {count} old appointments"
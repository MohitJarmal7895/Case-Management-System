from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

def send_appointment_notification(appointment, notification_type):
    """
    Send email notifications for appointments
    notification_type can be: 'created', 'updated', 'reminder', 'cancelled'
    """
    subject_templates = {
        'created': 'New Appointment Scheduled',
        'updated': 'Appointment Updated',
        'reminder': 'Appointment Reminder',
        'cancelled': 'Appointment Cancelled'
    }

    context = {
        'appointment': appointment,
        'notification_type': notification_type,
    }

    # Email to client
    client_subject = f"{subject_templates[notification_type]} - {appointment.title}"
    client_message = render_to_string('appointments/email/client_notification.html', context)
    
    send_mail(
        subject=client_subject,
        message=client_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.client.email],
        html_message=client_message
    )

    # Email to staff/attorney
    staff_subject = f"[Staff] {subject_templates[notification_type]} - {appointment.title}"
    staff_message = render_to_string('appointments/email/staff_notification.html', context)
    
    send_mail(
        subject=staff_subject,
        message=staff_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.STAFF_EMAIL],
        html_message=staff_message
    )

def send_appointment_reminders():
    """Send reminders for upcoming appointments"""
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    upcoming_appointments = Appointment.objects.filter(
        date_time__date=tomorrow.date(),
        status='SCHEDULED'
    )

    for appointment in upcoming_appointments:
        send_appointment_notification(appointment, 'reminder')
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import Case
from .models import EmailNotification
import uuid
from .logging import logger

@shared_task(bind=True, max_retries=3)
def send_case_notification_task(self, case_id, notification_type, additional_context=None, request_url=None):
    try:
        case = Case.objects.get(pk=case_id)
        
        template_map = {
            'filing': 'email/cases/filing.html',
            'update': 'email/cases/update.html',
        }
        
        subject_map = {
            'filing': f'New Case Filed - {case.title}',
            'update': f'Case Update - {case.title}',
        }

        context = {
            'case': case,
            'case_url': request_url + reverse('cases:case_detail', args=[case.pk])
        }
        
        if additional_context:
            context.update(additional_context)

        html_message = render_to_string(template_map[notification_type], context)
        
        send_mail(
            subject=subject_map[notification_type],
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[case.client.email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Successfully sent {notification_type} notification for case {case.pk}")
        return True

    except Exception as exc:
        logger.error(f"Failed to send {notification_type} notification for case {case_id}: {str(exc)}")
        self.retry(exc=exc, countdown=60 * 5)  # Retry after 5 minutes


@shared_task(bind=True, max_retries=3)
def send_case_notification_task(self, notification_id):
    notification = EmailNotification.objects.get(pk=notification_id)
    try:
        case = notification.case
        tracking_pixel = f'<img src="/track/email/{notification.tracking_id}/open.png" />'
        
        context = {
            'case': case,
            'case_url': f'/track/email/{notification.tracking_id}/click?url=' + 
                       reverse('cases:case_detail', args=[case.pk]),
            'tracking_pixel': tracking_pixel
        }
        
        if notification.additional_context:
            context.update(notification.additional_context)

        html_message = render_to_string(
            notification.template_name,
            context
        ) + tracking_pixel

        send_mail(
            subject=notification.subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient],
            html_message=html_message,
            fail_silently=False
        )
        
        notification.status = 'SENT'
        notification.save()
        logger.info(f"Successfully sent notification {notification.pk}")

    except Exception as exc:
        notification.status = 'FAILED'
        notification.error_message = str(exc)
        notification.save()
        logger.error(f"Failed to send notification {notification.pk}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * 5)
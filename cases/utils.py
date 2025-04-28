from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .logging import logger
from .tasks import send_case_notification_task

def send_case_notification(request, case, notification_type, additional_context=None):
    """
    Queue case-related email notifications
    notification_type can be: 'filing', 'update', 'status_change', 'hearing'
    """
    try:
        request_url = request.build_absolute_uri('/')[:-1]
        send_case_notification_task.delay(
            case.pk,
            notification_type,
            additional_context,
            request_url
        )
        logger.info(f"Queued {notification_type} notification for case {case.pk}")
        return True
    except Exception as e:
        logger.error(f"Failed to queue {notification_type} notification for case {case.pk}: {str(e)}")
        return False
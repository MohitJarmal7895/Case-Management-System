from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    try:
        send_mail(
            subject='Test Email from Legal Management System',
            message='This is a test email to verify the email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.STAFF_EMAIL],
            fail_silently=False,
        )
        return "Test email sent successfully!"
    except Exception as e:
        return f"Error sending test email: {str(e)}"

if __name__ == "__main__":
    print(test_email_configuration())
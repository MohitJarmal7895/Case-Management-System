from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Case, EmailNotification, NotificationPreference
from unittest.mock import patch

class NotificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.case = Case.objects.create(
            title='Test Case',
            client=self.user
        )
        self.client.login(username='testuser', password='testpass123')

    def test_email_tracking(self):
        notification = EmailNotification.objects.create(
            case=self.case,
            notification_type='filing',
            recipient='test@example.com'
        )
        
        # Test open tracking
        response = self.client.get(
            reverse('cases:track_email_open', args=[notification.tracking_id])
        )
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertEqual(notification.status, 'OPENED')
        
        # Test click tracking
        response = self.client.get(
            reverse('cases:track_email_click', args=[notification.tracking_id]),
            {'url': reverse('cases:case_detail', args=[self.case.pk])}
        )
        self.assertEqual(response.status_code, 302)
        notification.refresh_from_db()
        self.assertEqual(notification.status, 'CLICKED')

    @patch('cases.tasks.send_mail')
    def test_notification_sending(self, mock_send_mail):
        response = self.client.post(
            reverse('cases:case_create'),
            {'title': 'New Test Case'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_send_mail.called)

    def test_notification_preferences(self):
        response = self.client.post(
            reverse('cases:notification_preferences'),
            {'email_notifications': True}
        )
        self.assertEqual(response.status_code, 302)
        pref = NotificationPreference.objects.get(user=self.user)
        self.assertTrue(pref.email_notifications)

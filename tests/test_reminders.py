from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from reminders.models import Reminder


class ReminderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)

    def test_create_and_toggle_reminder(self):
        today = timezone.now().date()
        res = self.client.post(reverse('reminders:create'), {
            'title': 'Follow up with recruiter on HR round update',
            'reminder_type': 'Recruiter follow-up',
            'due_date': str(today),
            'priority': 'High',
            'description': 'Send polite status inquiry.'
        })
        self.assertEqual(res.status_code, 302)
        rem = Reminder.objects.get(user=self.user)
        self.assertEqual(rem.title, 'Follow up with recruiter on HR round update')
        self.assertFalse(rem.is_completed)

        # Toggle to completed via API
        toggle_res = self.client.post(
            reverse('reminders:toggle_api', args=[rem.pk]),
            data='{"completed": true}',
            content_type='application/json'
        )
        self.assertEqual(toggle_res.status_code, 200)
        rem.refresh_from_db()
        self.assertTrue(rem.is_completed)
        self.assertIsNotNone(rem.completed_at)

    def test_overdue_detection(self):
        yesterday = timezone.now().date() - timedelta(days=1)
        overdue_rem = Reminder.objects.create(
            user=self.user,
            title='Overdue follow-up',
            due_date=yesterday,
            is_completed=False
        )
        self.assertTrue(overdue_rem.is_overdue)

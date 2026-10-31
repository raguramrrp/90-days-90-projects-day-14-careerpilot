from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from opportunities.models import Company, Opportunity
from applications.models import Application
from reminders.models import Reminder
from documents.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile


class UserIsolationTests(TestCase):
    def setUp(self):
        # User A
        self.user_a = User.objects.create_user(username='user_a', password='PasswordA123!')
        self.comp_a = Company.objects.create(user=self.user_a, name='Secret Corp A')
        self.opp_a = Opportunity.objects.create(user=self.user_a, company=self.comp_a, title='Classified Role A')
        self.app_a = Application.objects.create(user=self.user_a, opportunity=self.opp_a, status='Applied')
        self.rem_a = Reminder.objects.create(user=self.user_a, title='Private Follow-up A', due_date='2026-11-10')
        self.doc_a = Document.objects.create(
            user=self.user_a,
            title='Confidential_Resume_A.pdf',
            file=SimpleUploadedFile("resume_a.pdf", b"candidate a data")
        )

        # User B
        self.user_b = User.objects.create_user(username='user_b', password='PasswordB123!')
        self.client_b = Client()
        self.client_b.force_login(self.user_b)

    def test_user_b_cannot_view_user_a_opportunity(self):
        res = self.client_b.get(reverse('opportunities:detail', args=[self.opp_a.pk]))
        self.assertEqual(res.status_code, 404)

    def test_user_b_cannot_view_user_a_application(self):
        res = self.client_b.get(reverse('applications:detail', args=[self.app_a.pk]))
        self.assertEqual(res.status_code, 404)

    def test_user_b_cannot_download_user_a_document(self):
        res = self.client_b.get(reverse('documents:download', args=[self.doc_a.pk]))
        self.assertEqual(res.status_code, 404)

    def test_user_b_cannot_toggle_user_a_reminder(self):
        res = self.client_b.post(
            reverse('reminders:toggle_api', args=[self.rem_a.pk]),
            data='{"completed": true}',
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 404)

    def test_user_b_export_contains_no_user_a_data(self):
        res = self.client_b.get(reverse('reports:export_applications_csv'))
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertNotIn('Secret Corp A', content)
        self.assertNotIn('Classified Role A', content)

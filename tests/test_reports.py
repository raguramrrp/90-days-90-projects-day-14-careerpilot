from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from opportunities.models import Company, Opportunity
from applications.models import Application


class ReportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)
        self.company = Company.objects.create(user=self.user, name='Zoho')
        self.opportunity = Opportunity.objects.create(
            user=self.user,
            company=self.company,
            title='Member Technical Staff'
        )
        self.application = Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status='Applied'
        )

    def test_csv_export(self):
        response = self.client.get(reverse('reports:export_applications_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Zoho', content)
        self.assertIn('Member Technical Staff', content)

    def test_excel_export(self):
        response = self.client.get(reverse('reports:export_applications_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('spreadsheetml.sheet', response['Content-Type'])
        self.assertTrue(len(response.content) > 0)

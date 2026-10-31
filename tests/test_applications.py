from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from opportunities.models import Company, Opportunity
from applications.models import Application, ApplicationStatusHistory


class ApplicationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)
        self.company = Company.objects.create(user=self.user, name='Razorpay')
        self.opportunity = Opportunity.objects.create(
            user=self.user,
            company=self.company,
            title='Backend SDE'
        )

    def test_application_creation_and_history(self):
        response = self.client.post(reverse('applications:create'), {
            'opportunity': self.opportunity.pk,
            'status': 'Applied',
            'application_date': '2026-11-01',
            'application_method': 'Company Portal',
            'recruiter_name': 'Ankit Verma',
            'notes': 'Submitted direct application.'
        })
        self.assertEqual(response.status_code, 302)
        app = Application.objects.get(user=self.user, opportunity=self.opportunity)
        self.assertEqual(app.status, 'Applied')

        # Check initial status history
        self.assertTrue(app.status_history.filter(new_status='Applied').exists())

    def test_status_update_via_api_and_history_logging(self):
        app = Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status='Applied'
        )

        # Update status to Technical Interview via AJAX API
        response = self.client.post(
            reverse('applications:update_status_api', args=[app.pk]),
            data='{"status": "Technical Interview", "notes": "Cleared OA with 100% score"}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        app.refresh_from_db()
        self.assertEqual(app.status, 'Technical Interview')

        # Check status history record created
        latest_history = app.status_history.latest('changed_at')
        self.assertEqual(latest_history.previous_status, 'Applied')
        self.assertEqual(latest_history.new_status, 'Technical Interview')
        self.assertIn('Cleared OA', latest_history.notes)

    def test_kanban_view_status(self):
        Application.objects.create(user=self.user, opportunity=self.opportunity, status='Assessment')
        res = self.client.get(reverse('applications:kanban'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Razorpay')
        self.assertContains(res, 'Assessment')

    def test_duplicate_application_prevention(self):
        # Create initial application
        Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status='Applied'
        )

        # Attempt to post a second application for the exact same opportunity
        response = self.client.post(reverse('applications:create'), {
            'opportunity': self.opportunity.pk,
            'status': 'Applied',
            'application_date': '2026-11-01',
            'application_method': 'Company Portal',
        })
        # Should NOT raise 500 IntegrityError; should either re-render form with error (200) or redirect (302)
        self.assertIn(response.status_code, [200, 302])
        # Only 1 application should exist in database
        self.assertEqual(Application.objects.filter(user=self.user, opportunity=self.opportunity).count(), 1)

    def test_create_view_with_existing_opportunity_id_redirects(self):
        app = Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status='Applied'
        )
        # Access create view with query param of already applied opportunity
        res = self.client.get(f"{reverse('applications:create')}?opportunity_id={self.opportunity.pk}")
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('applications:detail', args=[app.pk]))

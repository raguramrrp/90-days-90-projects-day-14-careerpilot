from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from opportunities.models import Company, Opportunity
from applications.models import Application
from analytics.services import calculate_kpis, get_analytics_charts_data, get_analytics_insights
from analytics.recommendations import get_career_recommendations


class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)
        self.company = Company.objects.create(user=self.user, name='Swiggy')
        self.opportunity = Opportunity.objects.create(
            user=self.user,
            company=self.company,
            title='Backend SDE',
            category='Software Engineering'
        )

    def test_kpis_calculation(self):
        Application.objects.create(
            user=self.user,
            opportunity=self.opportunity,
            status='Offer Received',
            application_date=timezone.now().date()
        )

        kpis = calculate_kpis(self.user)
        self.assertEqual(kpis['total_applications'], 1)
        self.assertEqual(kpis['offers_received'], 1)
        self.assertEqual(kpis['offer_conversion_rate'], 100.0)

    def test_charts_data_structure(self):
        data = get_analytics_charts_data(self.user)
        self.assertIn('pipeline_distribution', data)
        self.assertIn('category_distribution', data)
        self.assertIn('apps_by_month', data)

    def test_recommendation_engine(self):
        recs = get_career_recommendations(self.user)
        self.assertIsInstance(recs, list)

    def test_analytics_dashboard_view(self):
        res = self.client.get(reverse('analytics:dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Career Analytics Dashboard')

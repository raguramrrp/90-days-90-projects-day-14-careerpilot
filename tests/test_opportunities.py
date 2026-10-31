from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from opportunities.models import Company, Opportunity


class OpportunityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)
        self.company = Company.objects.create(
            user=self.user,
            name='Google India',
            website='https://careers.google.com'
        )
        self.opportunity = Opportunity.objects.create(
            user=self.user,
            company=self.company,
            title='Backend Architect Alpha',
            category='Software Engineering',
            employment_type='Full-time',
            work_mode='Hybrid',
            priority='High',
            source='LinkedIn'
        )

    def test_opportunity_create(self):
        response = self.client.post(reverse('opportunities:create'), {
            'company_name': 'Microsoft',
            'company_website': 'https://careers.microsoft.com',
            'title': 'Applied AI Engineer',
            'category': 'AI & Machine Learning',
            'employment_type': 'Full-time',
            'classification': 'Full-time',
            'work_mode': 'Remote',
            'source': 'Company website',
            'priority': 'Urgent',
            'interest_status': 'Interested',
            'is_accepting_applications': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Opportunity.objects.filter(title='Applied AI Engineer', company__name='Microsoft').exists())

    def test_opportunity_detail_and_update(self):
        response = self.client.get(reverse('opportunities:detail', args=[self.opportunity.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Backend Architect Alpha')

        update_res = self.client.post(reverse('opportunities:update', args=[self.opportunity.pk]), {
            'company_name': 'Google India',
            'title': 'Senior Systems Architect',
            'category': 'Software Engineering',
            'employment_type': 'Full-time',
            'classification': 'Full-time',
            'work_mode': 'Hybrid',
            'source': 'LinkedIn',
            'priority': 'Urgent',
            'interest_status': 'Saved',
            'is_accepting_applications': True,
        })
        self.assertEqual(update_res.status_code, 302)
        self.opportunity.refresh_from_db()
        self.assertEqual(self.opportunity.title, 'Senior Systems Architect')

    def test_opportunity_search_and_filter(self):
        # Create second opportunity with unique name
        opp2 = Opportunity.objects.create(
            user=self.user,
            company=self.company,
            title='Unique Data Scientist Beta',
            category='Data Analytics & BI',
            employment_type='Full-time',
            work_mode='Remote',
            source='Naukri'
        )

        # Search by title
        res = self.client.get(reverse('opportunities:list'), {'q': 'Unique Data Scientist Beta'})
        self.assertContains(res, 'Unique Data Scientist Beta')
        self.assertNotContains(res, 'Backend Architect Alpha')

        # Filter by category
        cat_res = self.client.get(reverse('opportunities:list'), {'category': 'Data Analytics & BI'})
        self.assertContains(cat_res, 'Unique Data Scientist Beta')
        self.assertNotContains(cat_res, 'Backend Architect Alpha')

    def test_duplicate_check_api(self):
        res = self.client.get(reverse('opportunities:check_duplicate_api'), {
            'company': 'Google India',
            'title': 'Backend Architect Alpha'
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['duplicate'])
        self.assertEqual(data['existing_id'], self.opportunity.pk)

    def test_opportunity_delete(self):
        res = self.client.post(reverse('opportunities:delete', args=[self.opportunity.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertFalse(Opportunity.objects.filter(pk=self.opportunity.pk).exists())

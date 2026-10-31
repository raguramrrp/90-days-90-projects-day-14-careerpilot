from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from opportunities.models import Company, Opportunity
from applications.models import Application
from interviews.models import Interview, InterviewChecklistItem


class InterviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)
        self.company = Company.objects.create(user=self.user, name='Atlassian')
        self.opportunity = Opportunity.objects.create(user=self.user, company=self.company, title='SDE 1')
        self.application = Application.objects.create(user=self.user, opportunity=self.opportunity, status='Technical Interview')

    def test_interview_create_seeds_checklist(self):
        response = self.client.post(reverse('interviews:create'), {
            'application': self.application.pk,
            'round_number': 1,
            'round_title': 'Round 1: DSA & Problem Solving',
            'interview_date': '2026-11-05',
            'mode': 'Online',
            'topics_to_prepare': 'Dynamic Programming, Trees, System Design',
            'outcome': 'Scheduled'
        })
        self.assertEqual(response.status_code, 302)
        intv = Interview.objects.get(application=self.application, round_number=1)
        self.assertEqual(intv.round_title, 'Round 1: DSA & Problem Solving')
        # Check that standard checklist was seeded
        self.assertEqual(intv.checklist_items.count(), len(InterviewChecklistItem.DEFAULT_ITEMS))

    def test_checklist_toggle_api(self):
        intv = Interview.objects.create(
            user=self.user,
            application=self.application,
            round_number=1,
            interview_date='2026-11-05'
        )
        item = InterviewChecklistItem.objects.create(
            interview=intv,
            item_text='Review Resume Projects',
            is_completed=False
        )

        res = self.client.post(
            reverse('interviews:toggle_checklist_api', args=[item.pk]),
            data='{"completed": true}',
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.is_completed)

    def test_preparation_notes_view(self):
        Interview.objects.create(
            user=self.user,
            application=self.application,
            round_number=1,
            interview_date='2026-10-20',
            outcome='Passed',
            questions_asked='Design LRU Cache in O(1)',
            personal_answers='Used Doubly Linked List + HashMap',
            areas_to_improve='Concurrency edge cases'
        )
        res = self.client.get(reverse('interviews:preparation_notes'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Design LRU Cache')
        self.assertContains(res, 'Doubly Linked List')

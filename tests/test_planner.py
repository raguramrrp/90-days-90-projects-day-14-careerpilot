from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from planner.models import CareerTask, CareerGoal
from applications.models import Application
from opportunities.models import Company, Opportunity


class PlannerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='user1',
            email='u1@example.com',
            password='TestPassword123!'
        )
        self.client.force_login(self.user)

    def test_task_create_and_toggle(self):
        today = timezone.now().date()
        res = self.client.post(reverse('planner:task_create'), {
            'title': 'Solve 2 DP problems on LeetCode',
            'category': 'Skill Development',
            'priority': 'High',
            'due_date': str(today)
        })
        self.assertEqual(res.status_code, 302)
        task = CareerTask.objects.get(user=self.user)
        self.assertEqual(task.title, 'Solve 2 DP problems on LeetCode')

        # Toggle via API
        toggle_res = self.client.post(
            reverse('planner:task_toggle_api', args=[task.pk]),
            data='{"completed": true}',
            content_type='application/json'
        )
        self.assertEqual(toggle_res.status_code, 200)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_goal_progress_calculation(self):
        today = timezone.now().date()
        goal = CareerGoal.objects.create(
            user=self.user,
            goal_type='Weekly',
            category='Applications',
            title='Apply to 3 product companies',
            target_count=3,
            period_start_date=today - timedelta(days=2),
            period_end_date=today + timedelta(days=5)
        )
        # Initially 0
        self.assertEqual(goal.current_progress, 0)
        self.assertEqual(goal.progress_percentage, 0)

        # Create 2 applications
        comp = Company.objects.create(user=self.user, name='Comp 1')
        opp1 = Opportunity.objects.create(user=self.user, company=comp, title='Role 1')
        opp2 = Opportunity.objects.create(user=self.user, company=comp, title='Role 2')
        Application.objects.create(user=self.user, opportunity=opp1, application_date=today)
        Application.objects.create(user=self.user, opportunity=opp2, application_date=today)

        # Progress should now reflect 2
        self.assertEqual(goal.current_progress, 2)
        self.assertEqual(goal.progress_percentage, 66)

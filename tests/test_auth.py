from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='candidate1',
            email='c1@example.com',
            password='TestPassword123!',
            first_name='Candidate',
            last_name='One'
        )

    def test_user_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login_and_logout(self):
        login_res = self.client.post(reverse('accounts:login'), {
            'username': 'candidate1',
            'password': 'TestPassword123!'
        })
        self.assertEqual(login_res.status_code, 302)

        logout_res = self.client.get(reverse('accounts:logout'))
        self.assertEqual(logout_res.status_code, 302)

    def test_unauthorized_access_redirects_to_login(self):
        unauth_client = Client()
        response = unauth_client.get(reverse('core:overview'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_update(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'preferred_roles': 'Backend Engineer, ML Engineer',
            'preferred_employment_types': 'Full-time',
            'preferred_work_modes': 'Remote',
            'follow_up_default_days': 10,
            'theme': 'dark',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.profile.theme, 'dark')
        self.assertEqual(self.user.profile.follow_up_default_days, 10)

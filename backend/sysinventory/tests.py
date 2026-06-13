from django.contrib.auth import get_user_model
from django.test import TestCase


class LoginApiTests(TestCase):
    def test_login_endpoint_accepts_json_credentials_without_csrf_token(self):
        User = get_user_model()
        User.objects.create_user(username='suporte', password='123master')

        response = self.client.post(
            '/api/v1/login/',
            {'username': 'suporte', 'password': '123master'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertEqual(response.json()['user']['username'], 'suporte')

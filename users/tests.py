from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

def make_user(email='test@test.com', password='pass1234', role='buyer', **kw):
    return User.objects.create_user(email=email, password=password, role=role,
                                    first_name='Test', last_name='User', **kw)

class RegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/register/'
        self.valid = {
            'email': 'new@test.com', 'password': 'pass1234',
            'first_name': 'New', 'last_name': 'User', 'role': 'buyer',
        }

    # ── happy paths ──────────────────────────────────────────────
    def test_register_buyer_returns_201(self):
        res = self.client.post(self.url, self.valid, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_seller_returns_201(self):
        data = {**self.valid, 'email': 'seller@test.com', 'role': 'seller'}
        res = self.client.post(self.url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_returns_access_and_refresh_tokens(self):
        res = self.client.post(self.url, self.valid, format='json')
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_register_returns_user_object_with_correct_role(self):
        res = self.client.post(self.url, self.valid, format='json')
        self.assertEqual(res.data['user']['role'], 'buyer')
        self.assertEqual(res.data['user']['email'], 'new@test.com')

    def test_password_is_not_returned_in_response(self):
        res = self.client.post(self.url, self.valid, format='json')
        self.assertNotIn('password', res.data.get('user', {}))

    # ── validation errors ─────────────────────────────────────────
    def test_duplicate_email_returns_400(self):
        make_user(email='new@test.com')
        res = self.client.post(self.url, self.valid, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password_returns_400(self):
        data = {**self.valid, 'password': '123'}
        res = self.client.post(self.url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_returns_400(self):
        data = {**self.valid, 'email': ''}
        res = self.client.post(self.url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_format_returns_400(self):
        data = {**self.valid, 'email': 'not-an-email'}
        res = self.client.post(self.url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/login/'
        self.user = make_user(email='login@test.com', password='pass1234', role='seller')

    # ── happy paths ──────────────────────────────────────────────
    def test_login_correct_credentials_returns_200(self):
        res = self.client.post(self.url, {'email': 'login@test.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_returns_access_and_refresh_tokens(self):
        res = self.client.post(self.url, {'email': 'login@test.com', 'password': 'pass1234'}, format='json')
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_returns_correct_user_role(self):
        res = self.client.post(self.url, {'email': 'login@test.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(res.data['user']['role'], 'seller')

    # ── auth failures ─────────────────────────────────────────────
    def test_wrong_password_returns_401(self):
        res = self.client.post(self.url, {'email': 'login@test.com', 'password': 'wrongpass'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_email_returns_401(self):
        res = self.client.post(self.url, {'email': 'ghost@test.com', 'password': 'pass1234'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_credentials_returns_401(self):
        res = self.client.post(self.url, {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class MeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/me/'
        self.user = make_user(email='me@test.com', role='buyer')

    def _get_token(self):
        res = self.client.post('/api/auth/login/', {'email': 'me@test.com', 'password': 'pass1234'}, format='json')
        return res.data['access']

    # ── happy paths ──────────────────────────────────────────────
    def test_me_with_valid_token_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_token()}')
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_me_returns_correct_user_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_token()}')
        res = self.client.get(self.url)
        self.assertEqual(res.data['email'], 'me@test.com')
        self.assertEqual(res.data['role'], 'buyer')

    def test_me_does_not_return_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self._get_token()}')
        res = self.client.get(self.url)
        self.assertNotIn('password', res.data)

    # ── auth failures ─────────────────────────────────────────────
    def test_me_without_token_returns_401(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_with_invalid_token_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer fake.token.here')
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTests(TestCase):
    def test_create_user_hashes_password(self):
        user = make_user()
        self.assertNotEqual(user.password, 'pass1234')
        self.assertTrue(user.check_password('pass1234'))

    def test_default_role_is_buyer(self):
        user = User.objects.create_user(email='x@test.com', password='pass1234',
                                        first_name='X', last_name='Y')
        self.assertEqual(user.role, 'buyer')

    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_str_representation(self):
        user = make_user(email='str@test.com', role='seller')
        self.assertIn('str@test.com', str(user))
        self.assertIn('seller', str(user))

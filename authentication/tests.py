import json
import secrets

from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, RequestsClient
from .models import Token
from accounts.models import CustomUser


def mocked_info():
    return {
        "day_of_week": 0,
        "timezone": "Asia/Tehran"
    }


def mocked_info_wrong():
    return False


class CheckAuthenticationHeader(object):

    def __init__(self, *args, **kwargs):
        super(CheckAuthenticationHeader, self).__init__(*args, **kwargs)
        self.url = None
        self.method = None
        self.data = None
        self.header = None
        self.client = RequestsClient()

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='MohammadJavad',
            password='MohammadJavad1380@@',
            phone_number='09122016216',
        )
        self.token = Token.objects.create(
            user=self.user,
            user_agent='Pycharm',
            key=secrets.token_hex(38),
        )

    def return_response(self):
        if self.method == 'POST':
            resp = self.client.post(self.url, self.data, headers=self.header)
        elif self.method == 'PUT':
            resp = self.client.put(self.url, self.data, headers=self.header)
        elif self.method == 'PATCH':
            resp = self.client.patch(self.url, self.data, headers=self.header)
        elif self.method == 'DELETE':
            resp = self.client.delete(self.url, self.data, headers=self.header)
        else:
            resp = self.client.get(self.url, self.data, headers=self.header)
        return resp

    def test_check_header(self):
        self.header = {
            'USER-TOKEN': '1234567890!@#$%^&*()ASDFGHJKL',
            'HTTP_USER_AGENT': 'Pycharm',
        }
        resp = self.return_response()
        self.assertEqual(resp.status_code, 403)


class GetTimeTest(CheckAuthenticationHeader, APITestCase):

    def __init__(self, *args, **kwargs):
        super(GetTimeTest, self).__init__(*args, **kwargs)
        self.url = reverse('get_time')
        self.method = 'GET'
        self.data = None
        self.header = None

    def setUp(self):
        super(GetTimeTest, self).setUp()

    @patch('authentication.views.get_response', mocked_info)
    def test_correct_time(self):
        self.header = {
            'USER-TOKEN': self.token.key,
            'HTTP_USER_AGENT': 'Pycharm',
        }
        resp = self.return_response()
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'timezone')

    @patch('authentication.views.get_response', mocked_info_wrong)
    def test_incorrect_time(self):
        self.header = {
            'USER-TOKEN': self.token.key,
            'HTTP_USER_AGENT': 'Pycharm',
        }
        resp = self.return_response()
        self.assertEqual(resp.status_code, 400)


class RegistrationTest(APITestCase):

    def __init__(self, *args, **kwargs):
        super(RegistrationTest, self).__init__(*args, **kwargs)
        self.client = RequestsClient()

    def test_registration(self):
        resp = self.client.post(reverse('registration'), data={
            'username': 'MohammadJavadShamloo',
            'phone_number': '09122016216',
            'password1': 'MohaJav1380@@',
            'password2': 'MohaJav1380@@',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 200)
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.username, 'MohammadJavadShamloo')

    def test_registration_wrong_type(self):
        resp = self.client.post(reverse('registration'), data={
            'username': 'MohammadJavadShamloo',
            'phone_number': '09122016216',
            'password1': '-------------',
            'password2': 'MohaJav1380@@',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 400)


class LoginTest(APITestCase):

    def __init__(self, *args, **kwargs):
        super(LoginTest, self).__init__(*args, **kwargs)
        self.client = RequestsClient()

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='MohammadJavadShamloo',
            phone_number='09122016216',
            password='MohaJav1380@&',
        )

    def test_login(self):
        resp = self.client.post(reverse('login'), data={
            'username': 'MohammadJavadShamloo',
            'password': 'MohaJav1380@&',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.token = self.user.tokens.last()
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, Token.objects.last().key)

    def test_login_wrong_password(self):
        resp = self.client.post(reverse('login'), data={
            'username': 'MohammadJavadShamloo',
            'password': 'MohaJav138111',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.token = self.user.tokens.last()
        self.assertEqual(resp.status_code, 403)

    def test_login_wrong_type_password(self):
        resp = self.client.post(reverse('login'), data={
            'username': 'MohammadJavadShamloo',
            'password': '---------',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.token = self.user.tokens.last()
        self.assertEqual(resp.status_code, 400)


class SendOtpTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super(SendOtpTest, self).__init__(*args, **kwargs)
        self.client = RequestsClient()

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='MohammadJavadShamloo',
            phone_number='09122016216',
            password='MohaJav1380@@',
        )

    def test_send_otp(self):
        resp = self.client.post(reverse('send_otp'), data={
            'phone_number': '09122016216',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Otp-Code')

    def test_send_otp_wrong_phone_number(self):
        resp = self.client.post(reverse('send_otp'), data={
            'phone_number': '01298639122016216',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 400)

    def test_send_otp_not_known_number(self):
        resp = self.client.post(reverse('send_otp'), data={
            'phone_number': '09386305256',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 404)


class ForgotPasswordTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super(ForgotPasswordTest, self).__init__(*args, **kwargs)
        self.client = RequestsClient()

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='MohammadJavadShamloo',
            phone_number='09122016216',
            password='MohaJav1380@@',
        )
        resp = self.client.post(reverse('send_otp'), data={
            'phone_number': self.user.phone_number,
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.otp_code = resp.json()['Otp-Code']

    def test_forgot_password(self):
        resp = self.client.patch(reverse('forgot_password'), data={
            'otp_code': self.otp_code,
            'phone_number': self.user.phone_number,
            'new_password1': 'MohaJavv1380@@',
            'new_password2': 'MohaJavv1380@@',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.user.check_password())

    def test_forgot_password_wrong_phone_number(self):
        resp = self.client.patch(reverse('forgot_password'), data={
            'otp_code': self.otp_code,
            'phone_number': '1119122016216',
            'new_password1': 'MohaJavv1380@@',
            'new_password2': 'MohaJavv1380@@',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 400)

    def test_forgot_password_empty_phone_number(self):
        resp = self.client.patch(reverse('forgot_password'), data={
            'otp_code': self.otp_code,
            'new_password1': 'MohaJavv1380@@',
            'new_password2': 'MohaJavv1380@@',
        }, headers={
            'HTTP_USER_AGENT': 'Pycharm',
        })
        self.assertEqual(resp.status_code, 400)

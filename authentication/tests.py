import secrets

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, RequestsClient
from .models import Token


class CheckAuthenticationTest(APITestCase):

    def __init__(self, url, method, data, *args, **kwargs):
        super(CheckAuthenticationTest, self).__init__(*args, **kwargs)
        self.url = url
        self.method = method
        self.client = RequestsClient()
        self.data = data if data else None

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='MohammadJavadShamloo',
            phone_number='09122016216',
            password='MohammadJavad1380@@',
        )
        self.token = Token.objects.create(
            key=secrets.token_hex(38),
            user_agent='Sample-User-Agent',
            user=self.user,
        )

    def test_authentication_header(self):
        resp = None
        if self.method == 'POST':
            resp = self.client.post(self.url, self.data, headers={
                'USER-TOKEN': self.token,
            })
        elif self.method == 'PUT':
            resp = self.client.put(self.url, self.data, headers={
                'USER-TOKEN': self.token,
            })
        elif self.method == 'PATCH':
            resp = self.client.patch(self.url, self.data, headers={
                'USER-TOKEN': self.token,
            })
        elif self.method == 'DELETE':
            resp = self.client.delete(self.url, self.data, headers={
                'USER-TOKEN': self.token,
            })
        else:
            resp = self.client.get(self.url, self.data, headers={
                'USER-TOKEN': self.token,
            })
        self.assertEqual(resp.status_code, 403)

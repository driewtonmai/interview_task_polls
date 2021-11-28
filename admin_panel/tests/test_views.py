import base64

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase

from polls.models import Poll
from admin_panel.views import PollListCreateAPIView, AdminLoginView


class PollListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('admin_panel:admin-polls-list-create')
        self.user = User.objects.create(username='user', is_staff=True, email='roflan@bk.ru')
        self.user.set_password('test_pass')
        self.user.save()
        self.poll = Poll.objects.create(name='New poll',
                                        description='good new poll',
                                        end_date='2022-10-30',
                                        created_by=self.user)

        self.poll2 = Poll.objects.create(name='New poll 2',
                                         description='good new poll 2',
                                         end_date='2022-10-29',
                                         created_by=self.user)
        self.view = PollListCreateAPIView().as_view()

    def test_polls_list_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_with_basic_auth(self):
        credentials = 'user:test_pass'
        base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Basic {base64_credentials}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_poll_POST(self):
        Poll.objects.all().delete()
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Test Poll', 'description': 'test poll desc.',
                'end_date': '2022-1-13', 'start_date': '2021-12-30'}
        response = self.client.post(self.url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Poll.objects.count(), 1)
        self.assertTrue(Poll.objects.filter(name='Test Poll').exists())


class AdminLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, email='roflan@bk.ru')
        user.set_password('test_pass')
        user.save()

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.url = reverse('admin_panel:admin-login')
        self.view = AdminLoginView().as_view()
        self.factory = APIRequestFactory()
        self.password = 'test_pass'

    def test_login(self):
        response = self.client.post(self.url, {'username': self.user.username,
                                               'password': self.password}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(self.url, {'username': self.user.username,
                                               'password': 'wrong_password'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_credentials(self):
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
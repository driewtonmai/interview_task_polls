import base64
import datetime
import io

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase

from polls.models import Poll
from admin_panel.views import PollListCreateAPIView, AdminLoginAPIView, PollDetailAPIView


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
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

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


class AdminLoginAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, email='roflan@bk.ru')
        user.set_password('test_pass')
        user.save()

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.url = reverse('admin_panel:admin-login')
        self.password = 'test_pass'
        self.view = AdminLoginAPIView().as_view()

    def test_login(self):
        response = self.client.post(self.url, {'username': self.user.username,
                                               'password': self.password}, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(self.url, {'username': self.user.username,
                                               'password': 'wrong_password'}, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_credentials(self):
        response = self.client.post(self.url, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class PollDetailAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, email='roflan@bk.ru')
        user.set_password('test_pass')
        user.save()
        Poll.objects.create(name='New poll',
                            description='good new poll',
                            start_date=datetime.date(2022, 3, 2),
                            end_date=datetime.date(2022, 3, 10),
                            created_by=user)

    def setUp(self):
        self.poll = Poll.objects.get(id=1)
        self.user = User.objects.get(id=1)
        self.url = reverse('admin_panel:admin-polls-retrieve', kwargs={'pk': 1})
        self.doesnt_exist_url = reverse('admin_panel:admin-polls-retrieve', kwargs={'pk': 20})
        self.password = 'test_pass'
        self.view = PollDetailAPIView().as_view()

    def test_detail_poll_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_detail_poll_GET_non_exist_poll(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.doesnt_exist_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_poll_GET_without_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_poll_PUT(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Опрос о коррупции",
            "description": "Пожалуйста ответьте на все вопросы.",
            "end_date": "2021-11-15",
        }
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_detail_poll_PUT_edit_start_date(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Опрос о коррупции',
            'description': 'Пожалуйста ответьте на все вопросы.',
            'end_date': '2021-11-15',
            'start_date': '2021-10-10',
        }
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_poll_DELETE(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        stream = io.BytesIO(response.content)
        response_status_code = JSONParser().parse(stream)

        self.assertEquals(response_status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Poll.objects.filter(pk=self.poll.pk).exists())


# class QuestionListCreateAPIViewTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):

import base64
import datetime
import io

from django.urls import reverse
from django.contrib.auth.models import User

import factory
from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase

from polls.models import Poll, Question
from polls.constants import TEXT, MULTI_SELECT, SELECT
from polls.tests.factories import PollFactory, ClientFactory, QuestionFactory, OptionChoicesFactory, UserFactory
from admin_panel.views import PollListCreateAPIView, AdminLoginAPIView, PollDetailAPIView, QuestionListCreateAPIView, \
    QuestionDetailAPIView


class PollListCreateAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('admin_panel:admin-polls-list-create')
        cls.user = UserFactory(username='user', is_staff=True)
        cls.user.set_password('test_pass')
        cls.user.save()
        PollFactory.create_batch(size=5, created_by=cls.user)
        cls.view = PollListCreateAPIView().as_view()

    def test_polls_list_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_polls_list_GET_without_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_with_basic_auth(self):
        credentials = 'user:test_pass'
        base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Basic {base64_credentials}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_poll_POST(self):
        self.client.force_authenticate(user=self.user)
        data = factory.build(dict, FACTORY_CLASS=PollFactory, name='Test Poll', created_by=None)
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Poll.objects.count(), 6)
        self.assertTrue(Poll.objects.filter(name='Test Poll').exists())

    def test_validate_start_end_dates_POST(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Test Poll',
                'description': 'test poll desc.',
                'end_date': '2021-10-9',
                'start_date': '2021-10-10'
                }
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminLoginAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('admin_panel:admin-login')
        cls.user = UserFactory(username='user', is_staff=True)
        cls.user.set_password('test_pass')
        cls.user.save()
        cls.password = 'test_pass'
        cls.view = AdminLoginAPIView().as_view()

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
        cls.url = reverse('admin_panel:admin-polls-retrieve', kwargs={'pk': 1})
        cls.non_exist_url = reverse('admin_panel:admin-polls-retrieve', kwargs={'pk': 99})
        cls.user = UserFactory(username='user', is_staff=True)
        cls.user.set_password('test_pass')
        cls.user.save()
        cls.password = 'test_pass'
        cls.poll = PollFactory(created_by=cls.user)
        cls.view = PollDetailAPIView().as_view()

    def test_detail_poll_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_detail_poll_GET_non_exist_poll(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.non_exist_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_poll_GET_without_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_poll_PUT(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Опрос о коррупции",
            "description": "Пожалуйста ответьте на все вопросы.",
            "end_date": "2022-11-15",
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


class QuestionListCreateAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = PollFactory()
        cls.url = reverse('admin_panel:admin-questions-list-create', kwargs={'polls_pk': cls.poll.id})
        cls.question_queryset = QuestionFactory.create_batch(size=5, poll=cls.poll)
        cls.user = UserFactory(username='user', is_staff=True)
        cls.view = QuestionListCreateAPIView().as_view()

        for question in cls.question_queryset:
            OptionChoicesFactory.create_batch(size=2, question=question)

    def test_question_list_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 5)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_question_list_GET_without_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_question_create_POST_type_select(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "text": "Что вы думаете о TypeScript?",
            "type": SELECT,
            "poll": "Обратная связь курса \"Методы оптимизации\"",
            "option_choices": [
                {
                    "text": "Хороший язык"
                },
                {
                    "text": "Не пользовался"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Question.objects.count(), 6)
        self.assertTrue(Question.objects.filter(text='Что вы думаете о TypeScript?').exists())

    def test_question_create_validator_without_option_choices_POST_type_select(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "text": "Что вы думаете о TypeScript?",
            "type": SELECT,
            "poll": "Обратная связь курса \"Методы оптимизации\"",
            "option_choices": [],
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_create_POST_type_text(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "text": "Что вы думаете о TypeScript?",
            "type": TEXT,
            "poll": "Обратная связь курса \"Методы оптимизации\"",

        }
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_question_create_validator_with_option_choice_POST_type_text(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "text": "Что вы думаете о TypeScript?",
            "type": TEXT,
            "poll": "Обратная связь курса \"Методы оптимизации\"",
            "option_choices": [
                {
                    "text": "Хороший язык"
                },
                {
                    "text": "Не пользовался"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('admin_panel:admin-questions-retrieve', kwargs={'polls_pk': 1, 'questions_pk': 1})
        cls.non_exist_url = reverse('admin_panel:admin-questions-retrieve', kwargs={'polls_pk': 1, 'questions_pk': 99})
        cls.user = UserFactory(username='user', is_staff=True)
        cls.user.set_password('test_pass')
        cls.user.save()
        cls.password = 'test_pass'
        cls.poll = PollFactory(created_by=cls.user)
        cls.question = QuestionFactory(poll=cls.poll, type=MULTI_SELECT)
        cls.view = QuestionDetailAPIView().as_view()

    def test_question_detail_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.resolver_match.func.__name__, self.view.__name__)

    def test_question_detail_GET_without_login(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_question_detail_GET_non_exist_question(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.non_exist_url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_question_detail_PUT(self):
        self.client.force_authenticate(user=self.user)
        print(self.question.text, self.question.poll, self.question.type)
        data = {
            "text": "Что вы думаете о Scala?",
            "type": 2,
            "option_choices": [
                {
                    "text": "Явное лучше чем неявное"
                },
                {
                    "text": "Производительность!"
                }
            ]
        }
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from polls.constants import TEXT
from polls.models import Client, Poll, Question, QUESTION_TYPES, OptionChoices, Answer


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Client.objects.create(login=12456)

    def test_login_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('login').verbose_name
        self.assertEquals(field_label, 'ID пользователя')

    def test_representation_to_string(self):
        client = Client.objects.first()
        expected_str = str(client.login)
        self.assertEquals(str(client), expected_str)


class PollTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, password='1234')
        Poll.objects.create(name='New poll',
                            description='good new poll',
                            start_date=datetime.date(2022, 3, 2),
                            end_date=datetime.date(2022, 3, 10),
                            created_by=user)

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.poll = Poll.objects.get(id=1)

    def test_representation_to_string(self):
        self.assertEquals(self.poll.__str__(), self.poll.name)

    def test_published_day_amount(self):
        published_day_amount = (self.poll.end_date - self.poll.start_date)
        self.assertEquals(self.poll.published_day_amount, published_day_amount)

    def test_validate_end_date(self):
        poll = Poll.objects.create(name='New poll',
                                   description='good new poll',
                                   start_date=datetime.date(2022, 5, 2),
                                   end_date=datetime.date(2022, 5, 1),
                                   created_by=self.user)
        with self.assertRaises(ValidationError):
            poll.full_clean()

    def test_verbose_name(self):
        verbose_name = self.poll._meta.verbose_name
        self.assertEquals(verbose_name, 'опрос')

    def test_verbose_name_plural(self):
        verbose_name_plural = self.poll._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Опросы')

    def test_ordering(self):
        ordering = self.poll._meta.ordering
        self.assertEquals(ordering, ['-created_at'])

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            Poll.objects.create(name='New poll',
                                description='good new poll',
                                start_date=datetime.date(2022, 3, 2),
                                end_date=datetime.date(2022, 3, 10),
                                created_by=self.user)


class QuestionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, password='1234')
        poll = Poll.objects.create(name='New poll',
                                   description='good new poll',
                                   start_date=datetime.date(2022, 3, 2),
                                   end_date=datetime.date(2022, 3, 10),
                                   created_by=user)
        Question.objects.create(text='how r u?', type=TEXT, poll=poll)

    def setUp(self):
        self.question = Question.objects.get(id=1)

    def test_representation_to_string(self):
        self.assertEquals(self.question.__str__(), self.question.text)


class OptionChoicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', is_staff=True, password='1234')
        poll = Poll.objects.create(name='New poll',
                                   description='good new poll',
                                   start_date=datetime.date(2022, 3, 2),
                                   end_date=datetime.date(2022, 3, 10),
                                   created_by=user)
        question = Question.objects.create(text='how r u?', type=TEXT, poll=poll)
        OptionChoices.objects.create(question=question)

    def setUp(self):
        self.option_choice = OptionChoices.objects.get(id=1)

    def test_representation_to_string(self):
        self.assertEquals(self.option_choice.__str__(), self.option_choice.text)

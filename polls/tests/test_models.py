import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .factories import ClientFactory, PollFactory, QuestionFactory, OptionChoicesFactory, AnswerFactory, \
    AnswerOptionsFactory, UserSelectedPollFactory


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_instance = ClientFactory()

    def test_login_label(self):
        field_label = self.client_instance._meta.get_field('login').verbose_name
        self.assertEquals(field_label, 'ID пользователя')

    def test_representation_to_string(self):
        expected_str = str(self.client_instance.login)
        self.assertEquals(self.client_instance.__str__(), expected_str)


class PollTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = PollFactory(name='New poll', start_date=datetime.date(2022, 3, 2))
        cls.user = User.objects.get(id=1)

    def test_representation_to_string(self):
        self.assertEquals(self.poll.__str__(), self.poll.name)

    def test_published_day_amount(self):
        published_day_amount = (self.poll.end_date - self.poll.start_date)
        self.assertEquals(self.poll.published_day_amount, published_day_amount)

    def test_validate_end_date(self):
        poll = PollFactory.build(name='New poll', start_date=datetime.date(2022, 5, 2),
                           end_date=datetime.date(2022, 5, 1))
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
            PollFactory(name='New poll', start_date=datetime.date(2022, 3, 2))


class QuestionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()

    def test_representation_to_string(self):
        self.assertEquals(self.question.__str__(), self.question.text)


class OptionChoicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.option_choice = OptionChoicesFactory()

    def test_representation_to_string(self):
        self.assertEquals(self.option_choice.__str__(), self.option_choice.text)


class AnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.answer = AnswerFactory()

    def test_representation_to_string(self):
        excepted_str = f'Ответ вопроса "{self.answer.question.text}"'
        self.assertEquals(self.answer.__str__(), excepted_str)


class AnswerOptionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.answer_option = AnswerOptionsFactory()

    def test_representation_to_string(self):
        excepted_str = f'Вариант "{self.answer_option.option_choice}"'
        self.assertEquals(self.answer_option.__str__(), excepted_str)


class UserSelectedPollTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_selected_poll = UserSelectedPollFactory(poll__id=1, client__id=1)

    def test_representation_to_string(self):
        self.assertEquals(self.user_selected_poll.__str__(),
                          self.user_selected_poll.poll.name)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            UserSelectedPollFactory(poll__id=1, client__id=1)

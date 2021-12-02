from django.contrib.auth.models import User
from django.utils import timezone

import factory.fuzzy
import factory
from  factory.django import DjangoModelFactory

from polls.models import Poll, Question, Answer, AnswerOptions, OptionChoices, QUESTION_TYPES, Client, UserSelectedPoll


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttributeSequence(lambda obj, n: f'{obj.first_name}_{obj.last_name}_{n}@gmail.com'.lower())


class PollFactory(DjangoModelFactory):
    class Meta:
        model = Poll

    name = factory.Sequence(lambda n: f'Poll #{n}')
    description = 'Very good poll'
    start_date = factory.LazyFunction(timezone.now().date)
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timezone.timedelta(days=10))
    draft = True
    created_by = factory.SubFactory(UserFactory)


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    text = 'Question text'
    type = factory.Iterator(QUESTION_TYPES, getter=lambda c: c[0])
    poll = factory.SubFactory(PollFactory)


class OptionChoicesFactory(DjangoModelFactory):
    class Meta:
        model = OptionChoices

    text = 'Option text'
    question = factory.SubFactory(QuestionFactory)


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    login = factory.Sequence(lambda n: n)


class UserSelectedPollFactory(DjangoModelFactory):
    class Meta:
        model = UserSelectedPoll

    poll = factory.SubFactory(PollFactory)
    client = factory.SubFactory(ClientFactory)


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    text = 'Answer choice'
    question = factory.SubFactory(QuestionFactory)
    user_selected_poll = factory.SubFactory(UserSelectedPollFactory)


class AnswerOptionsFactory(DjangoModelFactory):
    class Meta:
        model = AnswerOptions

    option_choice = factory.SubFactory(OptionChoicesFactory)
    answer = factory.SubFactory(AnswerFactory)



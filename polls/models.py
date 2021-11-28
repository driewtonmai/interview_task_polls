from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .constants import TEXT, SELECT, MULTI_SELECT


QUESTION_TYPES = (
    (TEXT, 'text'),
    (SELECT, 'select'),
    (MULTI_SELECT, 'multi-select'),
)


class Poll(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)
    description = models.TextField(verbose_name='описание')
    start_date = models.DateField(verbose_name='дата старта', default=timezone.now().today)
    end_date = models.DateField(verbose_name='дата окончания')
    draft = models.BooleanField(verbose_name='черновик', default=True)
    created_by = models.ForeignKey(User, verbose_name='автор', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Дата редактирования')

    def __str__(self):
        return self.name

    @property
    def published_day_amount(self):
        amount_days = (self.end_date - self.start_date)
        return amount_days

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'опрос'
        verbose_name_plural = 'Опросы'
        unique_together = ['name', 'start_date']


class Question(models.Model):
    text = models.TextField(verbose_name='текст')
    type = models.SmallIntegerField(verbose_name='тип вопроса', choices=QUESTION_TYPES, default=1)
    poll = models.ForeignKey(Poll, verbose_name='опрос', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class OptionChoices(models.Model):
    text = models.CharField(verbose_name='текст', max_length=250)
    question = models.ForeignKey(Question, verbose_name='вопрос', on_delete=models.CASCADE,
                                 related_name='option_choices')

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(verbose_name='текст', max_length=250, blank=True)
    question = models.ForeignKey(Question, verbose_name='вопрос', on_delete=models.CASCADE)
    user_selected_poll = models.ForeignKey('UserSelectedPoll', verbose_name='опрос', on_delete=models.CASCADE)

    def __str__(self):
        return f'Ответ вопроса "{self.question.text}"'


class AnswerOptions(models.Model):
    option_choice = models.ForeignKey(OptionChoices, verbose_name='вариант ответа', on_delete=models.CASCADE,
                                      null=True, blank=True)
    answer = models.ForeignKey(Answer, verbose_name='ответ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Вариант "{self.option_choice}"'


class Client(models.Model):
    login = models.BigIntegerField(verbose_name='ID пользователя', unique=True)

    def __str__(self):
        return str(self.login)


class UserSelectedPoll(models.Model):
    poll = models.ForeignKey(Poll, verbose_name='опрос', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.poll.name

    class Meta:
        unique_together = ['poll', 'client']




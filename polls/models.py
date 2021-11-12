from django.db import models
from datetime import date
from django.contrib.auth.models import User


QUESTION_TYPES = (
    (1, 'text'),
    (2, 'select'),
    (3, 'multi-select'),
)


class Poll(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)
    description = models.TextField(verbose_name='описание')
    start_date = models.DateField(verbose_name='дата старта', default=date.today())
    end_date = models.DateField(verbose_name='дата окончания')
    draft = models.BooleanField(verbose_name='черновик', default=True)
    created_by = models.ForeignKey(User, verbose_name='автор', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Дата редактирования')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'опрос'
        verbose_name_plural = 'Опросы'
        unique_together = ['name', 'created_at']


class Question(models.Model):
    text = models.TextField(verbose_name='текст')
    type = models.SmallIntegerField(verbose_name='тип вопроса', choices=QUESTION_TYPES, default=1)
    poll = models.ForeignKey(Poll, verbose_name='опрос', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class OptionChoices(models.Model):
    text = models.CharField(verbose_name='текст', max_length=250)

    def __str__(self):
        return self.text


class QuestionOptions(models.Model):
    option_choice = models.ManyToManyField(OptionChoices, verbose_name='вариант ответа')
    question = models.ForeignKey(Question, verbose_name='вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return f'Варианты ответа вопроса: "{self.question}"'


class Answer(models.Model):
    question_options = models.ForeignKey(QuestionOptions, verbose_name='вопрос', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='текст', max_length=250, blank=True)

    def __str__(self):
        return self.text


class UserSelectedPoll(models.Model):
    poll = models.ForeignKey(Poll, verbose_name='опрос', on_delete=models.CASCADE)
    passed_user = models.BigIntegerField(verbose_name='ID пользователя')

    def __str__(self):
        return self.poll.name

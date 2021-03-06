# Generated by Django 2.2.10 on 2021-11-14 17:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('polls', '0001_initial'), ('polls', '0002_auto_20211112_1206'), ('polls', '0003_auto_20211112_1849'), ('polls', '0004_auto_20211113_0930'), ('polls', '0005_auto_20211113_0945'), ('polls', '0006_auto_20211113_1328'), ('polls', '0007_auto_20211113_1346'), ('polls', '0008_answer_user_selected_poll'), ('polls', '0009_auto_20211114_1048'), ('polls', '0010_auto_20211114_1050'), ('polls', '0011_auto_20211114_1103'), ('polls', '0012_auto_20211114_1106'), ('polls', '0013_auto_20211114_1118'), ('polls', '0014_auto_20211114_1443'), ('polls', '0015_auto_20211114_1453'), ('polls', '0016_auto_20211114_1454'), ('polls', '0017_auto_20211114_1500'), ('polls', '0018_auto_20211114_1505')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('start_date', models.DateField(default=datetime.date(2021, 11, 14), verbose_name='дата старта')),
                ('end_date', models.DateField(verbose_name='дата окончания')),
                ('draft', models.BooleanField(default=True, verbose_name='черновик')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'опрос',
                'verbose_name_plural': 'Опросы',
                'ordering': ['-created_at'],
                'unique_together': {('name', 'created_at')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст')),
                ('type', models.SmallIntegerField(choices=[(1, 'text'), (2, 'select'), (3, 'multi-select')], default=1, verbose_name='тип вопроса')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll', verbose_name='опрос')),
            ],
        ),
        migrations.CreateModel(
            name='OptionChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250, verbose_name='текст')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option_choices', to='polls.Question', verbose_name='вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='UserSelectedPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='user_selected_polls', to='polls.Poll', verbose_name='опрос')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=250, verbose_name='текст')),
                ('question', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Question', verbose_name='вопрос')),
                ('user_selected_poll', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.UserSelectedPoll', verbose_name='опрос')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Answer', verbose_name='ответ')),
                ('option_choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.OptionChoices', verbose_name='вариант ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.BigIntegerField(unique=True, verbose_name='ID пользователя')),
            ],
        ),
        migrations.AddField(
            model_name='userselectedpoll',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Client', verbose_name='пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userselectedpoll',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll', verbose_name='опрос'),
        ),
        migrations.AlterUniqueTogether(
            name='userselectedpoll',
            unique_together={('poll', 'client')},
        ),
    ]

# Generated by Django 2.2.10 on 2021-11-19 09:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_squashed_0018_auto_20211114_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question', verbose_name='вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user_selected_poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.UserSelectedPoll', verbose_name='опрос'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 19, 9, 13, 47, 430954), verbose_name='дата старта'),
        ),
    ]
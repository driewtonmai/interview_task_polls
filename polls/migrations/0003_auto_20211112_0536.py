# Generated by Django 2.2.10 on 2021-11-12 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20211112_0533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionoptions',
            name='option_choice',
        ),
        migrations.AddField(
            model_name='questionoptions',
            name='option_choice',
            field=models.ManyToManyField(to='polls.OptionChoices', verbose_name='вариант ответа'),
        ),
    ]

# Generated by Django 2.2.10 on 2021-11-12 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question_options',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.QuestionOptions', verbose_name='вопрос'),
        ),
    ]

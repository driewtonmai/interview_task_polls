# Generated by Django 2.2.10 on 2021-11-25 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20211121_1624'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='poll',
            unique_together={('name', 'start_date')},
        ),
    ]

# Generated by Django 2.0.2 on 2018-03-07 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20180307_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='reporter',
        ),
    ]

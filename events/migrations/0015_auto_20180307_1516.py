# Generated by Django 2.0.2 on 2018-03-07 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_remove_event_reporter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventthreatactor',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventthreatactor',
            name='threat_actor',
        ),
        migrations.DeleteModel(
            name='EventThreatActor',
        ),
    ]

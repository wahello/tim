# Generated by Django 2.0.2 on 2018-03-02 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0006_auto_20180301_1505'),
        ('events', '0009_event_country'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventobservable',
            unique_together={('observable', 'event')},
        ),
    ]

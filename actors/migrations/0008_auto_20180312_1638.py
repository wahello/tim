# Generated by Django 2.0.2 on 2018-03-12 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_remove_event_targeted_organization'),
        ('actors', '0007_auto_20180312_1127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='actor',
            unique_together={('event', 'role')},
        ),
    ]

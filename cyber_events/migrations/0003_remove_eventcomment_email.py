# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-30 16:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyber_events', '0002_auto_20180130_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventcomment',
            name='email',
        ),
    ]

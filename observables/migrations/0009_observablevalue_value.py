# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-06 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0008_auto_20180206_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='observablevalue',
            name='value',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-06 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0013_auto_20180206_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='observablevalue',
            name='_my_date',
            field=models.DateField(db_column=b'my_date', default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

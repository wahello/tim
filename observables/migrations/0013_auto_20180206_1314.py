# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-06 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0012_auto_20180206_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observablevalue',
            old_name='value',
            new_name='_value',
        ),
    ]

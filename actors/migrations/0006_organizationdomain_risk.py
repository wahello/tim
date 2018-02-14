# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-14 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0005_auto_20180214_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationdomain',
            name='risk',
            field=models.CharField(choices=[('critical', 'critical'), ('high', 'high'), ('medium', 'medium'), ('low', 'low'), ('unknown', 'unknown')], default='unknown', max_length=10),
        ),
    ]

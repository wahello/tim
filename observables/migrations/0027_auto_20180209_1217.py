# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-09 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0026_auto_20180209_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observable',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
    ]
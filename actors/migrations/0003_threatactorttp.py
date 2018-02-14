# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-14 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ttp', '0001_initial'),
        ('actors', '0002_auto_20180213_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreatActorTTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threat_actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ttp', to='actors.ThreatActor')),
                ('ttp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor', to='ttp.TTP')),
            ],
        ),
    ]

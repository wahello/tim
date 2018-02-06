# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-30 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cyber_events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('doc_type', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to=b'documents/events/')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='document',
        ),
        migrations.AddField(
            model_name='eventdocument',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_document', to='cyber_events.Event'),
        ),
    ]

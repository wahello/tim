# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-13 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Constituent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituent_author', to='users.Account')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='constituent_type', to='actors.ActorType')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reporter_author', to='users.Account')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reporter_type', to='actors.ActorType')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ThreatActor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('first_seen', models.DateTimeField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=250, null=True)),
                ('import_name', models.CharField(blank=True, max_length=250, null=True)),
                ('hunting', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/threat_actor/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor_author', to='users.Account')),
                ('motive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor_motive', to='common.Motive')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor_type', to='actors.ActorType')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]

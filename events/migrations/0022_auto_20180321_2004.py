# Generated by Django 2.0.2 on 2018-03-21 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20180321_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]

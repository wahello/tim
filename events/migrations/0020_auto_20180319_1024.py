# Generated by Django 2.0.2 on 2018-03-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20180319_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='reference',
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
    ]
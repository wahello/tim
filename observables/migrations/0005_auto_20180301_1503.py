# Generated by Django 2.0.2 on 2018-03-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0004_auto_20180301_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stringvalue',
            name='value',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]

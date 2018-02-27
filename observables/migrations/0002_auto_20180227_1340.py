# Generated by Django 2.0.2 on 2018-02-27 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='observable',
            name='confidence',
            field=models.CharField(choices=[('high', 'high'), ('medium', 'medium'), ('low', 'low'), ('unknown', 'unknown')], default='unknown', max_length=10),
        ),
        migrations.AddField(
            model_name='observable',
            name='risk',
            field=models.CharField(choices=[('critical', 'critical'), ('high', 'high'), ('medium', 'medium'), ('low', 'low'), ('unknown', 'unknown')], default='unknown', max_length=10),
        ),
        migrations.AddField(
            model_name='observable',
            name='tlp',
            field=models.CharField(choices=[('red', 'red'), ('amber', 'amber'), ('green', 'green'), ('white', 'white')], default='red', max_length=10),
        ),
    ]
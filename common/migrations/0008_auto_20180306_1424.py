# Generated by Django 2.0.2 on 2018-03-06 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('common', '0007_auto_20180306_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='intentsion',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intentsion', to='users.Account'),
        ),
        migrations.AddField(
            model_name='killchain',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kill_chain', to='users.Account'),
        ),
        migrations.AddField(
            model_name='motive',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motive', to='users.Account'),
        ),
        migrations.AddField(
            model_name='reporter',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to='users.Account'),
        ),
        migrations.AddField(
            model_name='subject',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='users.Account'),
        ),
        migrations.AddField(
            model_name='subjecttype',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_type', to='users.Account'),
        ),
    ]

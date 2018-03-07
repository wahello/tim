# Generated by Django 2.0.2 on 2018-03-07 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_auto_20180307_1452'),
        ('ttps', '0001_initial'),
        ('events', '0015_auto_20180307_1516'),
        ('actors', '0002_auto_20180216_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('reporter', 'Reporter'), ('target', 'Target'), ('threat_actor', 'Threat Actor')], default='unknown', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='threatactor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='threatactor',
            name='motive',
        ),
        migrations.RemoveField(
            model_name='threatactor',
            name='type',
        ),
        migrations.RemoveField(
            model_name='threatactorttp',
            name='threat_actor',
        ),
        migrations.RemoveField(
            model_name='threatactorttp',
            name='ttp',
        ),
        migrations.AddField(
            model_name='organization',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='first_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='hunting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='import_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='motive',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threat_actor_motive', to='common.Motive'),
        ),
        migrations.AddField(
            model_name='organization',
            name='reference',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='ttp',
            field=models.ManyToManyField(blank=True, to='ttps.TTP'),
        ),
        migrations.DeleteModel(
            name='ThreatActor',
        ),
        migrations.DeleteModel(
            name='ThreatActorTTP',
        ),
    ]

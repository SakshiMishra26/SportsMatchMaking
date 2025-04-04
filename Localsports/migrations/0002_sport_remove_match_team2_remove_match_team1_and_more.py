# Generated by Django 5.1.4 on 2025-02-10 17:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localsports', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='match_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='match',
            name='score_team1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='score_team2',
        ),
        migrations.AddField(
            model_name='match',
            name='location',
            field=models.CharField(default='Pune', max_length=255),
        ),
        migrations.AddField(
            model_name='match',
            name='sport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Localsports.sport'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('skill_level', models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])),
                ('sports', models.ManyToManyField(to='Localsports.sport')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MatchRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='Pending', max_length=10)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localsports.sport')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='Localsports.userprofile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='Localsports.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='players',
            field=models.ManyToManyField(to='Localsports.userprofile'),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]

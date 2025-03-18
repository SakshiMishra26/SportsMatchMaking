# Generated by Django 5.1.4 on 2025-03-10 05:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Localsports', '0006_userprofile_alter_match_created_by_and_more'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Team',
        ),
        migrations.AlterField(
            model_name='match',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_matches', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='match',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_matches', to='accounts.userprofile'),
        ),
        migrations.RemoveField(
            model_name='matchrequest',
            name='date',
        ),
        migrations.RemoveField(
            model_name='matchrequest',
            name='team_size',
        ),
        migrations.RemoveField(
            model_name='matchrequest',
            name='time',
        ),
        migrations.AddField(
            model_name='matchrequest',
            name='accepted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_matches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matchrequest',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matchrequest',
            name='skill_level',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=20),
        ),
        migrations.AddField(
            model_name='matchrequest',
            name='sport_type',
            field=models.CharField(choices=[('Football', 'Football'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis'), ('Badminton', 'Badminton'), ('Cricket', 'Cricket')], default='Football', max_length=50),
        ),
        migrations.AlterField(
            model_name='matchrequest',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='matchrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matchnotification',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Localsports.matchrequest'),
        ),
        migrations.AddField(
            model_name='matchnotification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

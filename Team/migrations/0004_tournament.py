# Generated by Django 5.1.4 on 2025-03-16 12:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0003_team_location_team_skill_level'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sport_type', models.CharField(choices=[('Football', 'Football'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis'), ('Cricket', 'Cricket')], max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tournaments', to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(blank=True, related_name='tournaments', to='Team.team')),
            ],
        ),
    ]

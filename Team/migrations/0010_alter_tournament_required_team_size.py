# Generated by Django 5.1.4 on 2025-03-21 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0009_alter_tournament_required_team_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='required_team_size',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 5.1.4 on 2025-03-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0007_tournament_required_team_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='required_team_size',
            field=models.IntegerField(default=11, editable=False),
        ),
    ]

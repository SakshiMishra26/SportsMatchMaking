# Generated by Django 5.1.4 on 2025-03-11 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='sport_type',
            field=models.CharField(choices=[('Football', 'Football'), ('Basketball', 'Basketball'), ('Tennis', 'Tennis'), ('Badminton', 'Badminton'), ('Cricket', 'Cricket')], max_length=50),
        ),
    ]

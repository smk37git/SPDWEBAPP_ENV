# Generated by Django 5.1.5 on 2025-02-01 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MISC', '0002_announcementalert_alter_daylightsavingsalert_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementalert',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='announcementalert',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

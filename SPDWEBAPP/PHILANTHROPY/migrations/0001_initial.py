# Generated by Django 4.2.16 on 2025-02-01 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Philanthropy_Hours_Event_and_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('philanthropy_event_name', models.CharField(max_length=200)),
                ('philanthropy_event_title', models.CharField(help_text='short title of the event', max_length=100)),
                ('philanthropy_approval_status', models.CharField(choices=[('approved', 'Approved'), ('requested', 'Requested'), ('denied', 'Denied')], default='requested', help_text='choice between approved, requested, and denied', max_length=20)),
                ('philanthropy_event_hours', models.IntegerField()),
                ('philanthropy_event_date', models.DateField(help_text='The date the event occurred')),
                ('philanthropy_event_submission_request_date', models.DateTimeField(auto_now_add=True, help_text='When the event is submitted this updates')),
                ('philanthropy_event_submission_approval_date', models.DateTimeField(blank=True, help_text='When the event is approved this updates', null=True)),
                ('philanthropy_event_approver_name', models.CharField(blank=True, help_text='This is the name of the person who approved the event', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Philanthropy Hours Event',
                'verbose_name_plural': 'Philanthropy Hours Events',
                'ordering': ['-philanthropy_event_date'],
            },
        ),
    ]

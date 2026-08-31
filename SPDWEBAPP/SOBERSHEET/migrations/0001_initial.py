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
            name='SoberSheetSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sober_time_title', models.CharField(help_text='Short description of the sober time', max_length=100)),
                ('sober_time_date', models.DateField(help_text='The date the sober time occurred')),
                ('sober_time_approval_status', models.CharField(choices=[('approved', 'Approved'), ('requested', 'Requested'), ('denied', 'Denied')], default='requested', help_text='Submission status: approved, requested, or denied', max_length=20)),
                ('sober_time_submission_request_date', models.DateTimeField(auto_now_add=True, help_text='The date the sober time was submitted')),
                ('sober_time_submission_approval_date', models.DateTimeField(blank=True, help_text='The date the sober time was approved/denied', null=True)),
                ('sober_time_approver_name', models.CharField(blank=True, help_text='The name of the person who approved/denied the submission', max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sober Sheet Submission',
                'verbose_name_plural': 'Sober Sheet Submissions',
                'ordering': ['-sober_time_date', '-sober_time_submission_request_date'],
            },
        ),
    ]

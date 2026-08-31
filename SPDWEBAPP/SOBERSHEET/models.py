from django.db import models
from django.contrib.auth.models import User


class SoberSheetSubmission(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('requested', 'Requested'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sober_time_title = models.CharField(max_length=100, help_text='Short description of the sober time')
    sober_time_date = models.DateField(help_text='The date the sober time occurred')
    sober_time_approval_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested',
        help_text='Submission status: approved, requested, or denied'
    )
    sober_time_submission_request_date = models.DateTimeField(
        auto_now_add=True,
        help_text='The date the sober time was submitted'
    )
    sober_time_submission_approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date the sober time was approved/denied'
    )
    sober_time_approver_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='The name of the person who approved/denied the submission'
    )

    def __str__(self):
        return f"{self.sober_time_title} - {self.user.username}"

    class Meta:
        verbose_name = 'Sober Sheet Submission'
        verbose_name_plural = 'Sober Sheet Submissions'
        ordering = ['-sober_time_date', '-sober_time_submission_request_date']

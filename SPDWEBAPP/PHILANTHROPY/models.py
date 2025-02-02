from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Philanthropy_Hours_Event_and_Request(models.Model):
    
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('requested', 'Requested'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    philanthropy_event_title = models.CharField(max_length=100, help_text="short title of the event")
    philanthropy_approval_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested',
        help_text="choice between approved, requested, and denied"
    )
    philanthropy_event_hours = models.IntegerField()
    philanthropy_event_date = models.DateField(help_text="The date the event occurred")
    philanthropy_event_submission_request_date = models.DateTimeField(
        auto_now_add=True,
        help_text="When the event is submitted this updates"
    )
    philanthropy_event_submission_approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the event is approved this updates"
    )
    philanthropy_event_approver_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="This is the name of the person who approved the event"
    )

    def __str__(self):
        return f"{self.philanthropy_event_title} - {self.user.username}"

    class Meta:
        verbose_name = "Philanthropy Hours Event"
        verbose_name_plural = "Philanthropy Hours Events"
        ordering = ['-philanthropy_event_date']
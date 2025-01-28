from django.db import models

# Day Light Savings Model
class DayLightSavingsAlert(models.Model):
    is_active = models.BooleanField(default=True)
    custom_alert = models.CharField(max_length=255, blank=True)

    class Meta:
        name = "Day Light Savings Settings"
        name_plural = "Day Light Savings Settings"
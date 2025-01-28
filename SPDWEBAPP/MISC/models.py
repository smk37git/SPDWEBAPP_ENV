from django.db import models

# Day Light Savings Model
class DayLightSavingsAlert(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Day Light Savings Alert Settings"
        verbose_name_plural = "Day Light Savings Alert Settings"
    
    def __str__(self):
        return f"DLS Alert - Active: {self.is_active}"

    def custom_message(self):
        return f"DLS Alert - Active: {self.name}"
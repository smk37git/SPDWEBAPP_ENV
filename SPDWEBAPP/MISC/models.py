from django.db import models

# Day Light Savings Model
class DayLightSavingsAlert(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Dashboard Annoucement Alert Settings"
        verbose_name_plural = "Dashboard Annoucement Alert Settings"
    
    def __str__(self):
        return f"DLS Alert - Active: {self.is_active}"
from django.contrib import admin

# Register your models here.
from .models import DayLightSavingsAlert

@admin.register(DayLightSavingsAlert)
class DayLightSavingsAlertAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'custom_message']

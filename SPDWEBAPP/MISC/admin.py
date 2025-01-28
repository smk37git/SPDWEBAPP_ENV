from django.contrib import admin
from .models import DayLightSavingsAlert

@admin.register(DayLightSavingsAlert)
class DayLightSavingsAlertAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'name']
    fields = ['is_active', 'name']
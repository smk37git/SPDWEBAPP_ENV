from django.contrib import admin
from .models import SoberSheetSubmission


@admin.register(SoberSheetSubmission)
class SoberSheetSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'sober_time_title',
        'user',
        'sober_time_approval_status',
        'sober_time_date',
        'sober_time_submission_request_date',
    )
    list_filter = ('sober_time_approval_status', 'sober_time_date')
    search_fields = ('sober_time_title', 'user__username', 'user__brother_profile__firstName', 'user__brother_profile__lastName')

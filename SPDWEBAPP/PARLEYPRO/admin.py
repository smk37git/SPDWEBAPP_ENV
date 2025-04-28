from django.contrib import admin
from .models import *
# Register your models here.
#admin.site.register(Vote_Poll)

@admin.register(Vote_Poll)
class VotePollAdmin(admin.ModelAdmin):
    list_display = (
        'Vote_Poll_Name',
        'created_by',
        'Vote_Poll_Count_Yes',
        'Vote_Poll_Count_No',
        'Vote_Poll_Start',
        'Vote_Poll_End',
    )

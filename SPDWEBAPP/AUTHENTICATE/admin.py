from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from .models import Brother_Profile, Role, Major
from .models import *

class Brother_ProfileForm(forms.ModelForm):
    new_major = forms.CharField(required=False)

    class Meta:
        model = Brother_Profile
        fields = ('majors',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['new_major']:
            major, created = Major.objects.get_or_create(name=self.cleaned_data['new_major'])
            instance.majors.add(major)
        if commit:
            instance.save()
        return instance

class Brother_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profileImage', 'get_majors')

    def get_majors(self, obj):
        return ', '.join([major.name for major in obj.majors.all()])

    get_majors.short_description = 'Majors'

    def save_model(self, request, obj, form, change):
        if 'profileImage' in request.FILES:
            obj.profileImage = request.FILES['profileImage']
        obj.save()

class MajorAdmin(admin.ModelAdmin):
    list_display = ('name',)

User  = get_user_model()
admin.site.register(Brother_Profile, Brother_ProfileAdmin)
admin.site.register(Role)
admin.site.register(Major, MajorAdmin)
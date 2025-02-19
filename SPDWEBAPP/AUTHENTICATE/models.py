from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    ROLE_CHOICES = [
        ('EXEC', 'Executive Board'),
        ('NM_BOARD', 'New Member Board'),
        ('ACTIVE', 'Active Member'),
        ('ALUMNI', 'Alumni'),
        ('NEW_MEMBER', 'New Member'),
        ('SOCIAL_CHAIR', 'Social Chair'),
        ('RUSH_CHAIR', 'Rush Chair'),
        ('PHIL_CHAIR', 'Philanthropy Chair'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Major(models.Model):
    name = models.CharField(max_length=255, default='Unknown')

    def __str__(self):
        return self.name

class Brother_Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    roles = models.ManyToManyField(Role, blank=True)
    profileImage = models.ImageField(upload_to='profile_images', blank=True, null=True)
    majors = models.ManyToManyField(Major, blank=True)

    def __str__(self):
        return self.firstName
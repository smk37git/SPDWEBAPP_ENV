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
    profileImage = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    hometown = models.CharField(max_length=200, null=True, blank=True)
    pclass = models.CharField(max_length=50, null=True, blank=True)  # New field
    roles = models.ManyToManyField(Role)
    majors = models.ManyToManyField(Major, blank=True)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
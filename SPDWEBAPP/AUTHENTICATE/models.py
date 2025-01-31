from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    # Predefined role choices
    ROLE_CHOICES = [
        ('EXEC', 'Executive Board'),
        ('PLEDGE_BOARD', 'Pledge Board'),
        ('ACTIVE', 'Active Member'),
        ('ALUMNI', 'Alumni'),
        ('NEW_MEMBER', 'New Member'),
        ('SOCIAL_CHAIR', 'Social Chair'),
        ('RUSH_CHAIR', 'Rush Chair'),
    ]

    name = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

class Major(models.Model):
    MAJOR_CHOICES = [
        ('Biological Engineering', 'Biological Engineering'),
        ('Biomedical Engineering', 'Biomedical Engineering'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Computer Engineering', 'Computer Engineering'),
        ('Computer Science', 'Computer Science'),
        ('Data Science', 'Data Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Environmental Engineering', 'Environmental Engineering'),
        ('Industrial Engineering', 'Industrial Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Other', 'Other')
    ]
    name = models.CharField(max_length=100, choices=MAJOR_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Brother_Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    roles = models.ManyToManyField(Role, blank=True)
    profileImage = models.ImageField(upload_to='images/', null=True, blank=True)
    majors = models.ManyToManyField(Major, blank=True)

    def __str__(self):
        return self.firstName
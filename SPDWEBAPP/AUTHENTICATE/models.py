from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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
    pclass = models.CharField(max_length=50, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    majors = models.ManyToManyField(Major, blank=True)
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
        
    def save(self, *args, **kwargs):
        if self.profileImage:
            # Open the uploaded image
            img = Image.open(self.profileImage)
            
            # Set maximum size
            output_size = (300, 300)
            
            # Resize image while maintaining aspect ratio
            img.thumbnail(output_size)
            
            # Save the resized image
            output = BytesIO()
            img_format = 'JPEG' if self.profileImage.name.lower().endswith(('jpg', 'jpeg')) else 'PNG'
            img.save(output, format=img_format, quality=85)
            output.seek(0)
            
            # Replace the image field with resized image
            self.profileImage = InMemoryUploadedFile(
                output, 
                'ImageField',
                f"{self.profileImage.name.split('.')[0]}.{img_format.lower()}", 
                f'image/{img_format.lower()}',
                sys.getsizeof(output), 
                None
            )
            
        super().save(*args, **kwargs)
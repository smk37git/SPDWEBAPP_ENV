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
        ('RECRUITMENT_CHAIR', 'Recruitment Chair'),
        ('PHIL_CHAIR', 'Philanthropy Chair'),
        ('RISK_MGR', 'Risk Manager'),
        ('PRESIDENT', 'President'),
        ('INT_VP', 'Internal VP'),
        ('EXT_VP', 'External VP'),
        ('BUSINESS_MGR', 'Business Manager'),
        ('AFFAIRS_DIRECTOR', 'Director of Chapter Affairs'),
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
            try:
                img = Image.open(self.profileImage)
                output_size = (300, 300)
                img.thumbnail(output_size)
                
                output = BytesIO()
                # Use original format if possible, default to PNG
                img_format = getattr(img, 'format', 'PNG')
                img.save(output, format=img_format, quality=85)
                output.seek(0)
                
                self.profileImage = InMemoryUploadedFile(
                    output, 
                    'ImageField',
                    f"{self.profileImage.name.split('/')[-1].split('.')[0]}.{img_format.lower()}", 
                    f'image/{img_format.lower()}',
                    sys.getsizeof(output), 
                    None
                )
            except Exception as e:
                # Log the error for debugging
                print(f"Error processing image: {e}")
                pass
                
        super().save(*args, **kwargs)
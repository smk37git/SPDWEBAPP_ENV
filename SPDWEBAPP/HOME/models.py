from django.db import models

class BannerImage(models.Model):
    image = models.ImageField(upload_to='banners/', help_text='Upload a new banner image')

    def save(self, *args, **kwargs):
        # Delete existing BannerImage objects
        BannerImage.objects.all().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return  "Banner Image"
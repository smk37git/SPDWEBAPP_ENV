from django.db import models

class Member(models.Model):
    firstName = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.firstName

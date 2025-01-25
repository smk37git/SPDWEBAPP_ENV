from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Vote_Tracker(models.Model):
#     Vote_name = models.CharField(max_length=200, null=True, blank=True)
#     No_votes = models.IntegerField(null=True, default=0)
#     Yes_votes = models.IntegerField(null=True, default=0)

#     def __str__(self):
#         return self.Vote_name
    
class Brother_votes(models.Model):
    vote_catergories =(('Aye','Aye'),('Nay','Nay'),('No Vote','No Vote'))
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_vote_choice= models.CharField(max_length=200, null=True, choices=vote_catergories)

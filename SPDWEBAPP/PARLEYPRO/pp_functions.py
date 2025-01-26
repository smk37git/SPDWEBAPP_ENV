from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Brother_votes


def Poll_Page_Handling(request, all_votes):
    '''
    This is the logic for how votes are counted, 
    this is a function meant to handle interactions on poll index
    '''
    
    if 'reset' in request.POST:
                # Reset ALL votes to 'No Vote'
                all_votes.all().update(user_vote_choice='No Vote')
    else:
            vote, created = Brother_votes.objects.get_or_create(
            user=request.user,
            defaults={'user_vote_choice': 'No Vote'}  # Default value for new records
        )
            vote = Brother_votes.objects.get(user=request.user)
            if 'nay' in request.POST:
                vote.user_vote_choice = 'Nay'
                vote.save()
            if 'aye' in request.POST:
                vote.user_vote_choice = 'Aye'
                vote.save()
            
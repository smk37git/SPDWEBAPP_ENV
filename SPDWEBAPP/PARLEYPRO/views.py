from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Brother_votes


@login_required
def change_vote(request):
    # Get the specific vote object
    vote, created = Brother_votes.objects.get_or_create(
            user=request.user,
            defaults={'user_vote_choice': 'No Vote'}  # Default value for new records
        )
    # Check if the logged-in user owns this vote
    if request.method == 'POST':
        vote = Brother_votes.objects.get(user=request.user)
        if 'nay' in request.POST:
            vote.user_vote_choice = 'Nay'
            vote.save()
        if 'aye' in request.POST:
            vote.user_vote_choice = 'Aye'
            vote.save()

    #these variables pull together all the votes to inject into the scoreboard
    nay_votes = Brother_votes.objects.filter(user_vote_choice='Nay').count()
    aye_votes = Brother_votes.objects.filter(user_vote_choice='Aye').count()
    context = {'nay_votes':nay_votes,'aye_votes':aye_votes}
    # Redirect back to the page showing votes
    return render(request, 'parleypro_homepage.html',context)  # Replace with your actual URL name
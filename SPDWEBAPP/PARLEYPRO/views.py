from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Brother_votes
from .pp_functions import Poll_Page_Handling

@login_required
def change_vote(request):
   
    all_votes = Brother_votes.objects
    
    if request.method == 'POST':
       Poll_Page_Handling(request, all_votes) 

    #these variables pull together all the votes to inject into the scoreboard
    nay_votes = all_votes.filter(user_vote_choice='Nay').count()
    aye_votes = all_votes.filter(user_vote_choice='Aye').count()
    context = {'nay_votes':nay_votes,'aye_votes':aye_votes}
    # Redirect back to the page showing votes
    return render(request, 'parleypro_homepage.html',context)  # Replace with your actual URL name
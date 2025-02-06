from django.shortcuts import render,redirect
from AUTHENTICATE.models import * # Import Member from database
from PARLEYPRO.pp_decorators import requires_role
from MISC.models import AnnouncementAlert



# SPD AUTHENTICATE
def home(request):
  Brother_Profiles = Brother_Profile.objects.all()
  return render(request, 'HOME/home.html', {'Brother_Profiles': Brother_Profiles})

# Create your views here.
def ourHistory(request):
    # Count profiles that have the 'ACTIVE' role.
    num_actives = Brother_Profile.objects.filter(roles__name='ACTIVE').distinct().count()
    context = {
        'num_actives': num_actives,
    }
    return render(request, 'HOME/ourHistory.html', context)

def codeOfEthics(request):
  return render(request, 'HOME/codeOfEthics.html')

def rush(request):
  return render(request, 'HOME/rush.html')
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

def executive_board(request):
    # Check if the role exists and get its exact name
    exec_role = Role.objects.filter(name__iexact='EXEC').first()
    
    # Get all brothers with the Executive Board role using the correct role object
    exec_board_brothers = Brother_Profile.objects.filter(roles=exec_role).order_by('lastName')
    
    # Create a mapping of specific executive board positions with their order
    exec_positions = {
        'Hunter Wilson': {'title': 'President', 'order': 1},
        'Mitchell Allen': {'title': 'Internal Vice President', 'order': 2},
        'Sebastian Main': {'title': 'External Vice President', 'order': 3},
        'Ryaan Biddle': {'title': 'Secretary', 'order': 4},
        'Cole Herman': {'title': 'Business Manager', 'order': 5},
        'Ryan Sanner': {'title': 'Rush Chair', 'order': 6},
        'Lucas Brown': {'title': 'Philanthropy Chair', 'order': 7},
        'Barrett Keegan': {'title': 'Risk Manager', 'order': 8},
        'Matthew Schupp': {'title': 'Social Chair', 'order': 9}
    }
    
    # Add position and order attributes to each brother
    brothers_list = []
    for brother in exec_board_brothers:
        full_name = f"{brother.firstName} {brother.lastName}"
        position_info = exec_positions.get(full_name, {'title': 'Executive Member', 'order': 999})
        brother.position = position_info['title']
        brother.position_order = position_info['order']
        brothers_list.append(brother)
    
    # Sort the brothers list by position order
    brothers_list.sort(key=lambda x: x.position_order)
    
    context = {
        'exec_board_brothers': brothers_list,
        'page_title': 'Executive Board'
    }
    return render(request, 'HOME/executive_board.html', context)
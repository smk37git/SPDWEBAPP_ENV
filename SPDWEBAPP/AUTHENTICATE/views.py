from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  # User Registration
from .forms import CreateUserForm  # User Registration

from .models import * # Import Member from database
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .utils import contains_profanity

# Announcement Model
from MISC.models import AnnouncementAlert


# SPD AUTHENTICATE
def home(request):
  Brother_Profiles = Brother_Profile.objects.all()
  return render(request, 'AUTHENTICATE/home.html', {'Brother_Profiles': Brother_Profiles})

@login_required
def dashboard(request):
    announcements = AnnouncementAlert.objects.filter(is_active=True)
    context = {
        'announcements': announcements
    }
    return render(request, 'AUTHENTICATE/dashboard.html', context)

@login_required
def roster(request):
  Brother_Profiles = Brother_Profile.objects.all()
  return render(request, 'AUTHENTICATE/roster.html', {'Brother_Profiles': Brother_Profiles})

def ourHistory(request):
  return render(request, 'AUTHENTICATE/ourHistory.html')

def codeOfEthics(request):
  return render(request, 'AUTHENTICATE/codeOfEthics.html')

def rush(request):
  return render(request, 'AUTHENTICATE/rush.html')

def registerPage(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()

  context = {'form': form}
  return render(request, 'AUTHENTICATE/register.html', context)


def loginPage(request):
  if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('it posted')
        user = authenticate(request, username = username, password= password)
        if user is not None:
            login(request, user)
            print('it worked')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)  # Redirect to the URL they were trying to access
            return redirect('home')
        else:
            return redirect('login')
  
  context = {}
  print(request.user)
  return render(request, 'AUTHENTICATE/login.html', context)

def logoutUser(request):
    logout(request)
    return render(request, 'AUTHENTICATE/home.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password1')
        confirm_password = data.get('new_password2')
        
        user = request.user
        
        if not user.check_password(current_password):
            return JsonResponse({
                'success': False,
                'error': 'Current password is incorrect.'
            })
        elif new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'error': 'New passwords do not match.'
            })
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({
                'success': True
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method.'
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        firstname = request.POST.get('firstName') 
        lastname = request.POST.get('lastName')
        
        # Check all fields for profanity
        if contains_profanity(username):
            return JsonResponse({
                'success': False,
                'message': 'Username contains inappropriate language.'
            })
            
        if contains_profanity(firstname):
            return JsonResponse({
                'success': False, 
                'message': 'First name contains inappropriate language.'
            })
            
        if contains_profanity(lastname):
            return JsonResponse({
                'success': False,
                'message': 'Last name contains inappropriate language.'
            })
            
        # Update if clean
        user = request.user
        brother_profile = Brother_Profile.objects.get(user=user)
        
        user.username = username
        user.email = request.POST.get('email')
        user.save()
        
        brother_profile.firstName = firstname
        brother_profile.lastName = lastname
        brother_profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully!'
        })
        
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })

@login_required
def profile(request):
    brother_profile = Brother_Profile.objects.get(user=request.user)
    
    # Check if profile image exists and is accessible
    if brother_profile.profileImage:
        try:
            brother_profile.profileImage.url
        except:
            brother_profile.profileImage = None
            brother_profile.save()
    
    available_majors = Major.objects.all().order_by('name')
    context = {
        'brother_profile': brother_profile,
        'available_majors': available_majors,
        'page': 'profile'
    }
    return render(request, 'AUTHENTICATE/profile.html', context)

@login_required
def update_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_photo'):
        try:
            brother_profile = Brother_Profile.objects.get(user=request.user)
            
            # Delete old photo if exists and it's not the default
            if brother_profile.profileImage:
                old_path = brother_profile.profileImage.path
                if os.path.exists(old_path) and 'default_profile.png' not in old_path:
                    brother_profile.profileImage.delete()
            
            brother_profile.profileImage = request.FILES['profile_photo']
            brother_profile.save()
            
            return HttpResponseRedirect(reverse('profile'))
            
        except Exception as e:
            messages.error(request, f'Error updating profile photo: {str(e)}')
            
    return HttpResponseRedirect(reverse('profile'))

@login_required
def reset_photo(request):
    if request.method == 'POST':
        try:
            brother_profile = Brother_Profile.objects.get(user=request.user)
            if brother_profile.profileImage:
                # Delete the old photo file
                brother_profile.profileImage.delete()
            brother_profile.profileImage = None
            brother_profile.save()
            return JsonResponse({
                'success': True,
                'message': 'Profile photo reset successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request'
    })

@login_required
def update_majors(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_majors = data.get('majors', [])
        
        try:
            brother_profile = Brother_Profile.objects.get(user=request.user)
            brother_profile.majors.clear()
            
            for major_name in selected_majors:
                major, _ = Major.objects.get_or_create(name=major_name)
                brother_profile.majors.add(major)
            
            return JsonResponse({
                'success': True,
                'message': 'Majors updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def add_custom_major(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        major_name = data.get('major_name', '').strip()
        
        # Check for profanity
        if contains_profanity(major_name):
            return JsonResponse({
                'success': False,
                'message': 'Major name contains inappropriate language'
            })

        # Capitalize each word
        major_name = ' '.join(word.capitalize() for word in major_name.split())
        
        try:
            major, created = Major.objects.get_or_create(name=major_name)
            return JsonResponse({
                'success': True,
                'major_id': major.id,
                'major_name': major.name
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })
# Home goes below here

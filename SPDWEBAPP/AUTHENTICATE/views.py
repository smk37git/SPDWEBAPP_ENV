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


# SPD AUTHENTICATE
def home(request):
  Brother_Profiles = Brother_Profile.objects.all()
  return render(request, 'AUTHENTICATE/home.html', {'Brother_Profiles': Brother_Profiles})

@login_required
def dashboard(request):
  return render(request, 'AUTHENTICATE/dashboard.html')

@login_required
def roster(request):
  Brother_Profiles = Brother_Profile.objects.all()
  return render(request, 'AUTHENTICATE/roster.html', {'Brother_Profiles': Brother_Profiles})

def codeOfEthics(request):
  return render(request, 'AUTHENTICATE/codeOfEthics.html')


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
        user = request.user
        brother_profile = Brother_Profile.objects.get(user=user)
        
        # Update user info
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        
        # Update profile info
        brother_profile.firstName = request.POST.get('firstName')
        brother_profile.lastName = request.POST.get('lastName')
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
    try:
        brother_profile = Brother_Profile.objects.get(user=request.user)
    except Brother_Profile.DoesNotExist:
        # Create new profile if doesn't exist
        brother_profile = Brother_Profile.objects.create(
            user=request.user,
            firstName=request.user.first_name,
            lastName=request.user.last_name
        )
    
    context = {'brother_profile': brother_profile}
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
# Home goes below here

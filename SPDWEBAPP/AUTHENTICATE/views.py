from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  # User Registration
from .forms import CreateUserForm  # User Registration

from .models import * # Import Member from database
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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
            return redirect('home')
        else:
            return redirect('home')
  
  context = {}
  print(request.user)
  return render(request, 'AUTHENTICATE/login.html', context)


# Home goes below here

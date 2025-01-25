from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  # User Registration
from .forms import CreateUserForm  # User Registration

from .models import Member # Import Member from database
from django.contrib.auth import authenticate, login, logout


# SPD AUTHENTICATE
def home(request):
  members = Member.objects.all()
  return render(request, 'AUTHENTICATE/home.html', {'members': members})


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

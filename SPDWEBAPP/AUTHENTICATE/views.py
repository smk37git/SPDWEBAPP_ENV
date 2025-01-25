from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  # User Registration
from .forms import CreateUserForm  # User Registration

from .models import Member # Import Member from database


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
  context = {}
  return render(request, 'AUTHENTICATE/login.html', context)


# Home goes below here

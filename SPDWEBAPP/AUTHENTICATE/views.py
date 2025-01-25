from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm  # User Registration Import


# SPD AUTHENTICATE
def home_page(request):
  return render(request, 'AUTHENTICATE/home.html')


def registerPage(request):
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()

  context = {'form': form}
  return render(request, 'AUTHENTICATE/register.html', context)


def loginPage(request):
  context = {}
  return render(request, 'AUTHENTICATE/login.html', context)


# Home goes below here

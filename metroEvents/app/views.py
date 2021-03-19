from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.template import RequestContext, context
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

def logoutUser(request):
  logout(request)
  return render(request, 'app/home.html')

class LoginView(View):
  def get(self,request):
    if request.user.is_authenticated:
      return redirect('app:user')
    return render(request, 'app/home.html')
    

  def post(self, request):
    print("hello")
    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username = username, password = password)

      if user is not None:
        login(request, user)
        return redirect('app:user')
      else:
        messages.info(request, "Username or password is incorrect!")
    context = {}
    return render(request, 'app:login', context)

class RegistrationView(View):
  def get(self,request):
    form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'app/registration.html', context)
  
  def post(self, request):
    form = CreateUserForm(request.POST)
    print("form is valid: " , form.is_valid())
    if form.is_valid():
      form.save()
      return redirect('app:login')
    print(form.errors)
    return HttpResponse("error!")


class CreateEventView(View):
  def get(self,request):
    context = {}
    return render(request, 'app/createEvent.html', context)

class RegularUserView(View):
  def get(self, request):
    if request.user.is_authenticated:
      context = {"authenticated" : True}
      return render(request, 'app/regularUserDashboard.html', context)
    return render(request, 'app/home.html')
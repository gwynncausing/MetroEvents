from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm
from django.template import RequestContext, context

# Create your views here.

class LoginView(View):
  def get(self,request):
    return render(request, 'app/home.html')

  def post(self, request):
    form = LoginForm(request.POST)
    print("form is valid: " , form.is_valid())
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return HttpResponse("Sucessfully logged in")
    print(form.errors)
    return HttpResponse("error!")

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
    #form = CreateEventForm()

   # context = {'form': form}
    return render(request, 'app/createEvent.html', context)
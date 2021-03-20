from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CreateEventForm
from django.template import RequestContext, context
from django.contrib import messages
from datetime import datetime, date


from django.contrib.auth.forms import UserCreationForm
from app.models import *

# Create your views here.

def logoutUser(request):
  logout(request)
  return redirect('app:login')

class LoginView(View):
  def get(self,request):
    if request.user.is_authenticated:
      currentUser = request.user
      if not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return redirect('app:organizer')
      elif currentUser.is_superuser:
        return redirect('app:administrator')
      else:
        return HttpResponse("wrong na")
    return render(request, 'app/home.html')
    

  def post(self, request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username = username, password = password)

    if user is not None:
      currentUser = user
      login(request, user)
      if not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return redirect('app:organizer')
      elif currentUser.is_superuser:
        return redirect('app:administrator')
      else:
        return HttpResponse("wrong na")
    else:
      messages.info(request, "Username or password is incorrect!")
    return render(request, 'app/home.html')

class RegistrationView(View):
  def get(self,request):
    if request.user.is_authenticated:
      return redirect('app:user')
    form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'app/registration.html', context)
  
  def post(self, request):
    form = UserCreationForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
      form.save()
      return redirect('app:login')
    print(form.errors)
    return HttpResponse("error!")

class RegularUserView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      if currentUser.is_superuser:
        return redirect('app:admin')
      elif not currentUser.is_staff:
        events = Event.objects.all()
        context = {'events': events}
        return render(request, 'app/regularUserDashboard.html', context)
      elif currentUser.is_staff:
        return redirect('app:organizer')
      else:
        return HttpResponse("wrong na")
    return render(request, 'app/home.html')

  def post(self, request):
    if 'requestToJoin' in request.POST:
      print(request.POST.get('event-id'))
      return redirect('app:user')

class CreateEventView(View):
  def get(self,request):
    context = {}
    return render(request, 'app/createEvent.html', context)
  
  def post(self, request):
    form = CreateEventForm(request.POST)
    if form.is_valid():
      title = request.POST.get("eventtitle")
      type = request.POST.get("eventtype")
      description = request.POST.get("description")
      datetime_start = request.POST.get("startdate")
      datetime_end = request.POST.get("enddate")
      # upvotes = 
      # participants = 

      form = Event(title = title, type = type, description = description, datetime_start = datetime_start, datetime_end = datetime_end)
      
      form.save()

      print("Event successfully created.")
      return HttpResponse('success')

    else:
      return HttpResponse('error')

class AdminDashboardView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      if currentUser.is_superuser:
        return render(request, 'app/adminDashboard.html')
      elif not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return redirect('app:organizer')
      else:
        return HttpResponse("wrong na")
    return HttpResponse("wrong na")


class OrgDashboardView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      # DO NOT DELETE THIS -----------------------------------
      # title = 'test'
      # type = 'test'
      # description = 'none'
      # upvotes = 0
      # dateee = date.today()
      # event = Event.objects.create(title = title, type = type, description = description, datetime_start = dateee, datetime_end= dateee, upvotes = upvotes)
      # print('current user: ', currentUser.id)
      # organizer = Organizer.objects.create(organizer_id = currentUser.id)
      # print(currentUser.is_staff)
      # currentUser.is_staff = True
      # currentUser.save()
      # DO NOT DELETE THIS -----------------------------------
      print('yay')
      if currentUser.is_superuser:
          return redirect('app:administrator')
      elif not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return render (request, 'app/orgDashboard.html')
      else:
        return HttpResponse("wrong na")
    return HttpResponse("wrong na")
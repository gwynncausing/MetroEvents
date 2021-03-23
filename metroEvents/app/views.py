from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.template import RequestContext, context
from django.contrib import messages
from datetime import datetime, date


from django.contrib.auth.forms import UserCreationForm
from app.models import *

# Create your views here.


def format_date(objects):
    for object in objects:
        object.datetime_start = object.datetime_start.strftime("%Y-%m-%d")
        object.datetime_end = object.datetime_end.strftime("%Y-%m-%d")

def logoutUser(request):
  logout(request)
  return redirect('app:login')

class LoginView(View):
  def get(self,request):
    if request.user.is_authenticated:
      currentUser = request.user
      if currentUser.is_superuser:
        return redirect('app:admin')
      elif not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return redirect('app:organizer')
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
      if currentUser.is_superuser:
        return redirect('app:admin')
      elif currentUser.is_staff:
        return redirect('app:organizer')
      elif not currentUser.is_staff:
        return redirect('app:user')
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
    messages.info(request, 'Your password must be between 8 and 30 characters.')
    messages.info(request, 'Your password must contain at least one uppercase, numeric and special character.')
    return redirect('app:registration')

class RegularUserView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      # if currentUser.is_superuser:
      #   return redirect('app:admin')
      # elif not currentUser.is_staff:
      events = Event.objects.all()
      myEvents = Event.objects.filter(participants = currentUser)
      context = {
        'events': events,
        'myEvents': myEvents,
      }
      return render(request, 'app/regularUserDashboard.html', context)
      # elif currentUser.is_staff:
      #   return redirect('app:organizer')
    else:
      return redirect('app:login')
    return render(request, 'app/home.html')

  def post(self, request):
    if 'requestToJoin' in request.POST:
      print(request.POST.get('event-id'))
      req = Request.objects.filter(user = request.user, requestType = "Join Event")
      if req:
        messages.info(request, "You have already requested to join the event.")
        return redirect('app:user')
      reqJoin = Request.objects.create(user = request.user, requestType = "Join Event")
      
      messages.info(request, "You have requested to join the event, you will received a notification once the organizer approve your request .")
    elif 'requestToBecomeOrg' in request.POST:
      print(request.user.id)
      req = Request.objects.filter(user = request.user, requestType = "Promote to Organizer", status = "Accepted")
      if req:
        messages.info(request, "You have already requested to become an organizer.")
        return redirect('app:user')
      reqOrg = Request.objects.create(user = request.user, requestType = "Promote to Organizer")
      
      messages.info(request, "You have requested to become an organizer, you will be redicted to an organizer page once you are a organizer.")
    elif 'submitUpvote' in request.POST:
      myeventid = request.POST.get('myevent-id')
      event = Event.objects.get(id = myeventid)

      btnradio = request.POST.get('btnradio')

      if btnradio == "upvote":
        event.upvotes = event.upvotes + 1
        event.save()
      elif btnradio == "downvote":
        event.upvotes = event.upvotes - 1
        event.save()
      messages.info(request, 'Upvote submitted successfully!')
    elif 'submitComment' in request.POST:
      myeventid = request.POST.get('myevent-id')
      event = Event.objects.get(id = myeventid)

      title = request.POST.get('review-title')
      comments = request.POST.get('comments')
      print(title, comments)
      
      review = Review.objects.create(title = title, comments = comments)
      event.review.add(review)
      event.save()
      messages.info(request, 'Review submitted successfully!')
    return redirect('app:user')



class CreateEventView(View):
  def get(self, request):
    if request.user.is_authenticated:
      if request.user.is_superuser or request.user.is_staff:
        currentUser = request.user
        return render(request, 'app/createEvent.html')
    return redirect('app:login')
  
  def post(self, request):
      organizer = Organizer.objects.get(organizer_id = request.user)
      title = request.POST.get("eventtitle")
      type = request.POST.get("eventtype")
      description = request.POST.get("description")
      datetime_start = request.POST.get("startdate")
      datetime_end = request.POST.get("enddate")
      event = Event.objects.create(title = title, type = type, description = description, datetime_start = datetime_start, datetime_end= datetime_end)
      organizer.event.add(event)

      print("Event successfully created.")
      messages.info(request, 'An event '+ title + ' has been created')
      if request.user.is_superuser:
        return redirect('app:admin')
      elif request.user.is_staff:
        return redirect('app:organizer')
      else:
        return redirect('app:login')

class AdminDashboardView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      if currentUser.is_superuser:
        req = Request.objects.filter(requestType = "Promote to Organizer", status = "For Review")
        events = Event.objects.all()
        users = User.objects.all()
        context = {
          'requests' : req,
          'events': events,
          'users': users,
        }
        return render(request, 'app/adminDashboard.html', context)
      elif not currentUser.is_staff:
        return redirect('app:user')
      elif currentUser.is_staff:
        return redirect('app:organizer')
      else:
        return redirect('app:login')
    return redirect('app:login')

  def post(self, request):
    if 'acceptOrg' in request.POST:
      print("hello", request.POST.get("request-id"))
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.status = "Accepted"
      req.datetime_reply = datetime.datetime.now()
      req.replied_by = request.user
      user = req.user
      user.is_staff = True
      req.save()
      user.save()
      print(user)
    if 'denyOrg' in request.POST:
      print("world")
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.status = "Denied"
      req.datetime_reply = datetime.datetime.now()
      req.replied_by = request.user
      req.save()
    return redirect('app:admin')


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

      # events = Event.objects.all()
      
  
      # if currentUser.is_superuser:
      #   return redirect('app:admin')
      
      if currentUser.is_staff or currentUser.is_superuser:
        organizer = Organizer.objects.get(organizer_id = currentUser)
        myEvents = Event.objects.filter(organizer = organizer)
        format_date(myEvents)
        context = {
          'myEvents': myEvents,
        }
        return render (request, 'app/orgDashboard.html', context)
      elif not currentUser.is_staff:
        return redirect('app:user')
      else:
        return redirect('app:login')
    return redirect('app:login')

  def post(self, request):
    if 'UpdateBtn' in request.POST:
      id = request.POST.get("event-id")
      title = request.POST.get("eventtitle")
      type = request.POST.get("eventtype")
      description = request.POST.get("description")
      datetime_start = request.POST.get("startdate")
      datetime_end = request.POST.get("enddate")
      print(id, title, type, description, datetime_start, datetime_end)
      Event.objects.filter(id=id).update(title=title, type = type, description = description, datetime_start = datetime_start, datetime_end = datetime_end)
    elif 'DeleteBtn' in request.POST:
      print('delete')
      id = request.POST.get("event-id")
      Event.objects.get(id = id).delete()
    
    return redirect('app:organizer')

 def post(self, request):
    if 'acceptParticipants' in request.POST:
      print("hello", request.POST.get("request-id"))
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.status = "Accepted"
      req.save()
    if 'denyParticipants' in request.POST:
      print("world")
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.status = "Denied"
      req.save()
    return redirect('app:organizer')

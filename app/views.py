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
      user = User.objects.get(username = request.POST.get('username'))
      user.email = request.POST.get('email')
      user.first_name = request.POST.get('firstname')
      user.last_name = request.POST.get('lastname')
      user.save()
      notification = Notification.objects.create()
      notification.title = "New Account!"
      notification.description = "Hello there! Welcome to 9 Metro Events"
      notification.datetime = datetime.datetime.now()
      notification.user.add(user)
      notification.save()

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
      myEvents = Event.objects.filter(participants = currentUser)
      events = Event.objects.exclude(participants = currentUser)
      notifications = Notification.objects.filter(user = currentUser).order_by('-datetime')
      context = {
        'myEvents': myEvents,
        'events': events,
        'notifications': notifications,
      }
      return render(request, 'app/regularUserDashboard.html', context)
      # elif currentUser.is_staff:
      #   return redirect('app:organizer')
    else:
      return redirect('app:login')
    return render(request, 'app/home.html')

  def post(self, request):
    if 'requestToJoin' in request.POST:
      eventid = request.POST.get('event-id')
      print()
      req = Request.objects.filter(user = request.user, requestType = "Join Event", event_id = eventid)
      if req:
        messages.info(request, "You have already requested to join the event.")
        return redirect('app:user')
      reqJoin = Request.objects.create(user = request.user, requestType = "Join Event", event_id = eventid)
      
      messages.info(request, "You have requested to join the event, you will received a notification once the organizer approve your request .")

    elif 'requestToBecomeOrg' in request.POST:
      print(request.user.id)
      req = Request.objects.filter(user = request.user, requestType = "Promote to Organizer", status = "For Review")
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
      print(datetime_start)
      print(datetime_end)
      event = Event.objects.create(title = title, type = type, description = description, datetime_start = datetime_start, datetime_end= datetime_end)
      print(event.datetime_start)
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
        notifications = Notification.objects.filter(user = currentUser).order_by('-datetime')
        format_date(events)
        context = {
          'requests' : req,
          'events': events,
          'users': users,
          'notifications': notifications,
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
    userid = request.POST.get("user-id")
    user = User.objects.get(id = userid)
    notification = Notification.objects.create()
    if 'acceptOrg' in request.POST:
      requestid = request.POST.get("request-id")

      req = Request.objects.get(id = requestid)
      organizer = Organizer.objects.create(organizer_id = userid)

      req.status = "Accepted"
      req.datetime_reply = datetime.datetime.now()
      req.replied_by = request.user

      user = req.user
      user.is_staff = True
      
      organizer.save()
      req.save()
      user.save()

      notification.title = "You are now an Organizer!"
      notification.description = "You can now access Organizer Dashboard!"
      notification.datetime = datetime.datetime.now()
      notification.user.add(user)
      notification.save()
    if 'denyOrg' in request.POST:
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.status = "Denied"
      req.datetime_reply = datetime.datetime.now()
      req.replied_by = request.user
      req.save()

      notification.title = "Organizer request denied."
      notification.description = "Your request has been denied by an administrator"
      notification.datetime = datetime.datetime.now()
      notification.user.add(user)
      notification.save()
    return redirect('app:admin')


class OrgDashboardView(View):
  def get(self, request):
    if request.user.is_authenticated:
      currentUser = request.user
      if currentUser.is_staff or currentUser.is_superuser:
        organizer = Organizer.objects.get(organizer_id = currentUser)
        myEvents = Event.objects.filter(organizer = organizer)

        requests = Request.objects.filter(event_id__in = myEvents, status = "For Review")
        format_date(myEvents)

        notifications = Notification.objects.filter(user = currentUser).order_by('-datetime')
        context = {
          'myEvents': myEvents,
          'requests': requests,
          'notifications': notifications,
        }
        return render (request, 'app/orgDashboard.html', context)
      elif not currentUser.is_staff:
        return redirect('app:user')
      else:
        return redirect('app:login')
    return redirect('app:login')

  def post(self, request):
    organizer = request.user
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

      organizer = Organizer.objects.get(organizer_id = request.user)
      event = Event.objects.get(id = id)
      participants = event.participants.all()
      print(organizer)
      print(event)
      print(participants)

      notification = Notification.objects.create()

      notification.title = "Event " + event.title + " has been cancelled"
      notification.description = "The event has been cancelled due to some problems occurred"
      notification.datetime = datetime.datetime.now()
      notification.user.add(*participants)
      notification.save()

      event.delete()

    if 'acceptParticipant' in request.POST:
      event = Event.objects.get(id = request.POST.get("event-id"))
      req = Request.objects.get(id = request.POST.get("request-id"))
      user = User.objects.get(id = request.POST.get("user-id"))
      event.participants.add(user)
      req.replied_by = organizer
      req.datetime_reply = datetime.datetime.now()
      req.status = "Accepted"
      req.save()

      notification = Notification.objects.create()
      notification.title = "Join event request accepted"
      notification.description = "You can now join the " + event.title
      notification.datetime = datetime.datetime.now()
      notification.user.add(user)
      notification.save()
    if 'denyParticipant' in request.POST:
      req = Request.objects.get(id = request.POST.get("request-id"))
      req.replied_by = organizer
      req.datetime_reply = datetime.datetime.now()
      req.status = "Denied"
      req.save()
    return redirect('app:organizer')
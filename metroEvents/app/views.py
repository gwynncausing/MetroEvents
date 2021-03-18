from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.

class LoginView(View):
  def get(self,request):
    return render(request, 'app/home.html')

class RegistrationView(View):
  def get(self,request):
    return render(request, 'app/registration.html')

class CreateEventView(View):
  def get(self,request):
    return render(request, 'app/createEvent.html')
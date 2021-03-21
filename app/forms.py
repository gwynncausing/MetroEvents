# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']


class CreateEventForm(forms.ModelForm):
  class Meta:
    model = Event
    # fields = ['title', 'type', 'description', 'datetime_start', 'datetime_end']
    fields = "__all__"
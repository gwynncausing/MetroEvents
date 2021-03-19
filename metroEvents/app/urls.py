from django.urls import path
from . import views as app_views
from django.contrib.auth.views import LoginView

app_name = 'app'

urlpatterns = [
  path('login/', app_views.LoginView.as_view(), name = "login"),
  path('register/', app_views.RegistrationView.as_view(), name = "registration"),
  path('createEvent/', app_views.CreateEventView.as_view(), name = "createEvent")
]
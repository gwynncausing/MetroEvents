from django.urls import path
from . import views as app_views
from django.contrib.auth.views import LoginView

app_name = 'app'

urlpatterns = [
  path('logout/', app_views.logoutUser, name = "logout"),
  path('', app_views.LoginView.as_view(), name = "login"),
  path('register/', app_views.RegistrationView.as_view(), name = "registration"),
  path('user/', app_views.RegularUserView.as_view(), name = "user"),
  path('createEvent/', app_views.CreateEventView.as_view(), name = "create_event"),
  path('administrator/', app_views.AdminDashboardView.as_view(), name = "admin"),
  path('organizer/', app_views.OrgDashboardView.as_view(), name = "organizer"),
]
from django.urls import path
from app import views as app_views

app_name = 'app'

urlpatterns = [
  path('', app_views.LoginView.as_view(), name = "login"),
]
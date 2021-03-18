from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Address(models.Model):
    # user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    barangay = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    province = models.CharField(max_length = 50)

    def __str__(self):
        return self.barangay + ", " + self.city + ", " + self.province

class User(AbstractBaseUser):
    USER_TYPE = (
        ('Regular', 'Regular'),
        ('Organizer', 'Organizer'),
        ('Admin', 'Admin'),
    )
    
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    username = models.CharField(max_length = 30, unique = True, null = True)
    password = models.CharField(max_length = 30, default = "123")
    password = models.CharField(max_length = 40, null = True)
    date_joined = models.DateField(auto_now_add = True, null = True)
    address =  models.ForeignKey(Address, on_delete=models.SET_NULL, null = True, blank = True)
    usertype = models.CharField(max_length = 30, null = True, choices = USER_TYPE, default = "Regular")

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Event(models.Model):
    # organizer = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    title = models.CharField(max_length = 45)
    type = models.CharField(max_length = 45)
    description = models.CharField(max_length = 100)
    datetime_start = models.DateTimeField(auto_now_add = True, blank = True)
    datetime_end = models.DateTimeField(auto_now_add = True, blank = True)
    upvotes = models.IntegerField(default = 0, blank = True, null = True)
    participants = models.ManyToManyField(User, blank = True)
    
    def __str__(self):
        return self.title

class Request(models.Model):
    REQUEST_TYPE = (
        ('Join Event', 'Join Event'),
        ('Promote to Organizer', 'Promote to Organizer'),
        ('Promote to Admin', 'Promote to Admin'),
    )
    REQUEST_STATUS = (
        ('For Review', 'For Review'),
        ('Accepted', 'Accepted'),
        ('Denied', 'Denied'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    requestType = models.CharField(max_length = 30, null = True, choices = REQUEST_TYPE, default = "Join Event")
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 100)
    status = models.CharField(max_length = 30, null = True, choices = REQUEST_STATUS, default = "For Review")
    datetime_request = models.DateTimeField(auto_now_add = True, blank = True)
    datetime_reply = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.requestType + " - " + str(self.id)

class Organizer(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    datePromoted = models.DateField(auto_now_add = True, blank = True)
    request = models.ManyToManyField(Request, blank = True)
    event = models.ManyToManyField(Event, blank = True)

    def __str__(self):
        return self.organizer_Id.username

class Administrator(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    datePromoted = models.DateField(auto_now_add = True, blank = True)
    request = models.ManyToManyField(Request, blank = True)

    def __str__(self):
        return self.admin_id.username

class Notification(models.Model):
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 100)
    datetime  = models.DateTimeField(auto_now_add = True, blank = True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null = True, blank = True)

# class User_Has_Events(models.Model):
#     event_id = models.IntegerField()
#     user_id = models.IntegerField()

# class User_Upvotes_Event(models.Model):
#     user_id = models.IntegerField()
#     event_id = models.IntegerField()

# class User_Reviews_Event(models.Model):
#     user_id = models.IntegerField()
#     event_id = models.IntegerField()
#     title = models.CharField(max_length = 100)
#     description = models.CharField(max_length = 100)

# class Organizer_Event(models.Model):
#     organizer_event_id = models.IntegerField()
#     event_id = models.IntegerField()

# class User_Has_Request(models.Model):
#     user_id = models.IntegerField()
#     request_id = models.IntegerField()

# class Administrator_Manages_User(models.Model):
#     admin_id = models.IntegerField()
#     user_id = models.IntegerField()
#     action = models.CharField(max_length = 100)
#     action_datetime = models.DateTimeField()

# class User_Notification(models.Model):
#     notification_id = models.IntegerField()
#     user_id = models.IntegerField()
    
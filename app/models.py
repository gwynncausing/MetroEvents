from django.db import models
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Create your models here.

# class Address(models.Model):
#     # user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
#     barangay = models.CharField(max_length = 50)
#     city = models.CharField(max_length = 50)
#     province = models.CharField(max_length = 50)

#     def __str__(self):
#         return self.barangay + ", " + self.city + ", " + self.province

# class MyUser(BaseUserAdmin):
#     requests = models.ManyToManyField(Requests, blank = True)
#     events = models.ManyToManyField(Events, blank = True)
#     def __str__(self):
#         return self.username

class Review(models.Model):
    title = models.CharField(max_length = 45, blank = True, null = True)
    comments = models.CharField(max_length = 45, blank = True, null = True)

class Event(models.Model):
    # organizer = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    title = models.CharField(max_length = 45, blank = True, null = True)
    type = models.CharField(max_length = 45, blank = True, null = True)
    description = models.CharField(max_length = 100, blank = True, null = True)
    datetime_start = models.DateField(default=timezone.now(), blank = True, null = True)
    datetime_end = models.DateField(default=timezone.now(), blank = True, null = True)
    upvotes = models.IntegerField(default = 0, blank = True, null = True)
    review = models.ManyToManyField(Review, blank = True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True, related_name = "+")
    requestType = models.CharField(max_length = 30, null = True, choices = REQUEST_TYPE, default = "Join Event")
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null = True, blank = True, related_name = "+")

    status = models.CharField(max_length = 30, null = True, choices = REQUEST_STATUS, default = "For Review")
    datetime_request = models.DateTimeField(auto_now_add = True, blank = True)
    datetime_reply = models.DateTimeField(blank = True, null = True)
    replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name = "+")

    def __str__(self):
        return self.requestType + " - " + str(self.id)

class Organizer(models.Model):
    organizer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default = 0)
    datePromoted = models.DateField(auto_now_add = True, blank = True)
    event = models.ManyToManyField(Event, blank = True)

    def __str__(self):
        return self.organizer.username

class Administrator(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default = 0)
    datePromoted = models.DateField(auto_now_add = True, blank = True)

    def __str__(self):
        return self.admin.username

class Notification(models.Model):
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 100)
    datetime  = models.DateTimeField(auto_now_add = True, blank = True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null = True, blank = True)
    user = models.ManyToManyField(User, blank = True)

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
    
from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.ForeignKey('app.User',on_delete=models.PROTECT)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    date_created= models.DateTimeField()
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    birthdate = models.DateField()
    #address = models.CharField(max_length = 50)
    #userType = models.CharField(max_length = 50)

class Address(models.Model):
    userId =  models.ForeignKey('app.User',on_delete=models.PROTECT)
    barangay = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    province = models.CharField(max_length = 50)

class UserType(models.Model):
    userId =  models.ForeignKey('app.User',on_delete=models.PROTECT)
    name = models.CharField(max_length = 50)

class User_Has_Events(models.Model):
    event_id = models.IntegerField(max_length=200)
    user_id = models.IntegerField(max_length=200)

class User_Upvotes_Event(models.Model):
    user_id = models.IntegerField(max_length=200)
    event_id = models.IntegerField(max_length=200)

class User_Reviews_Event(models.Model):
    user_id = models.IntegerField(max_length=200)
    event_id = models.IntegerField(max_length=200)
    title = models.CharField(max_lenght = 100)
    description = models.CharField(max_length = 100)

class Organizer(models.Model):
    organizer_Id = models.IntegerField(max_length=200)
    datePromoted = models.DateField()

class Organizer_Event(models.Model):
    organizer_event_id = models.IntegerField(max_length=200)
    event_id = models.IntegerField(max_length=200)

class Event(models.Model):
    event_id = models.ForeignKey('app.User',on_delete=models.PROTECT)
    title = models.CharField(max_lenght = 45)
    eventType = models.CharField(max_lenght = 45)
    description = models.CharField(max_length = 100)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    upvotes = models.IntegerField(max_length=200)

class User_Has_Request(models.Model):
    user_id = models.IntegerField(max_length=200)
    request_id = models.IntegerField(max_length=200)

class Request(models.Model):
    request_id = models.ForeignKey('app.User',on_delete=models.PROTECT)
    requestType = models.CharField(max_lenght = 45)
    description = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)
    datetime_request = models.DateTimeField()
    datetime_reply = models.DateTimeField()

class Administrator(models.Model):
    admin_id = models.IntegerField(max_length=200)
    datePromoted = models.DateTimeField()

class Administrator_Manages_User(models.Model):
    admin_id = models.IntegerField(max_length = 200)
    user_id = models.IntegerField(max_length = 200)
    action = models.CharField(max_length = 100)
    action_datetime = models.DateTimeField()

class User_Notification(models.Model):
    notification_id = models.IntegerField(max_length = 200)
    user_id = models.IntegerField(max_length = 200)

class Notification(models.Model):
    notification_id = models.ForeignKey('app.User',on_delete=models.PROTECT)
    title = models.CharField(max_lenght = 45)
    description = models.CharField(max_length = 100)
    datetime  = models.DateTimeField()
    request_id = models.models.IntegerField()

class User_Type(models.Model):
    user_type_id = models.ForeignKey('app.User',on_delete=models.PROTECT)
    name = models.CharField(max_length = 50)


    
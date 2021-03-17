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
    address = models.CharField(max_length = 50)
    userType = models.CharField(max_length = 50)
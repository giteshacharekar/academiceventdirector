from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from events.models import Post, eventComment
# Create your models here.
# Database ----> Excel workbook
# Models In Django ----> Table  --------> Sheet

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email

class Convocation(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    batchcourse = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    currentwork = models.TextField()
    attendstatus = models.CharField(max_length=255)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'ceremony update from ' + self.name + ' - ' + self.name

class eventlike(models.Model):
    id = models.AutoField(primary_key=True)
    
    srno= models.IntegerField(default=0)
    user = models.CharField(max_length=50)

    def __str__(self):
        return 'Register from ' + ' - ' + self.user

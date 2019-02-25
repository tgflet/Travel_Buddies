from django.db import models
from datetime import datetime as dt
import re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['name'])<1:
            errors['name']="All fields are required"
        elif len(postData['name'])<3:
            errors['name']="Name should be at least three characters"
        if len(postData['username'])<1:
            errors['username']="All fields are required"
        elif len(postData['username'])<3:
            errors['username']="Name should be at least three characters"
        elif str.isalpha(postData["username"])==False:
            errors['username']="Name cannot contain numbers"
        if len(postData['email'])<1:
            errors['email']="All fields are required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']="Please enter a valid email"
        elif User.objects.filter(email=postData['email']):
            errors['email']="Enter a unique email"
        if len(postData['pass'])<1:
            errors['pass']="All fields are required"
        elif len(postData['pass'])< 8:
            errors['pass']="Password should be at least eight characters"
        if postData['pass2']!=postData['pass']:
            errors['pass2']="Passwords don't match"
        
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postDATA):
        errors={}
        today=dt.now()
        if len(postDATA['dest'])<1:
            errors['dest']="All fields are required"
        if len(postDATA['desc'])<1:
            errors['desc']="All fields are required"
        if len(postDATA['start'])<1:
            errors['start']="All fields are required"
        if len(postDATA['end'])<1:
            errors['end']="All fields are required"
        if len(postDATA['start'])>1:
            a=dt.strptime(postDATA['start'], "%Y-%m-%d")
            if today>a:
                errors['start']="Trip must be at future date"
        if len(postDATA['start'])>1 and len(postDATA['end'])>1:
            a=dt.strptime(postDATA['start'], "%Y-%m-%d")
            b=dt.strptime(postDATA['end'], "%Y-%m-%d")
            if a>b:
                print("End date cannot be before start date")
                errors['end']="End date cannot be before start date"
        return errors


class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination=models.CharField(max_length=255)
    description=models.TextField()
    start=models.DateField()
    end=models.DateField()
    travelers=models.ManyToManyField(User, related_name="trips")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TripManager()

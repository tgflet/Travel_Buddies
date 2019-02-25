from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Trip
import bcrypt, re

def index(request):
    return render(request,'app_one/index.html')
def join(request):
    errors=User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/main')
    else:
        hash=bcrypt.hashpw(request.POST['pass'].encode(),bcrypt.gensalt())
        name=f"{request.POST['name']}"
        username=f"{request.POST['username']}"
        create=User.objects.create(name=name,username=username,email=request.POST['email'],password=hash.decode())
        request.session['user']=create.id
        print(request.session['user'])
        messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
        return redirect('/travels')
def verify(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['id']):
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/main')
    elif len(request.POST['id'])<1:
        messages.error(request, 'User could not be logged in',extra_tags="login")
        return redirect('/main')
    else:
        filtered=User.objects.filter(email=request.POST['id'])
        if filtered:
            result=User.objects.get(email=request.POST['id'])
            if bcrypt.checkpw(request.POST['pass'].encode(), result.password.encode()):
                request.session['user']=result.id
                messages.success(request, 'Successively Registered. Welcome!',extra_tags="welcome")
                return redirect('/travels')
            else:
                messages.error(request, 'User could not be logged in',extra_tags="login")
                return redirect('/main')
        else:
            messages.error(request, 'User could not be logged in',extra_tags="login")
            return redirect('/main')
def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out',extra_tags="out")
    return redirect('/main')
def dash(request):
    if 'user' in request.session:
        number=int(request.session['user'])
        userid=User.objects.get(id=number)
        trips=Trip.objects.filter(travelers=userid)
        others=Trip.objects.exclude(travelers=userid)
        context={
            "profile" : userid,
            "my_plans" : trips,
            "other_plans":others,
        }
        return render(request, 'app_one/dashboard.html',context)
    else:
        return redirect('/main')
def plan(request):
    return render(request,'app_one/add.html')
def add(request):
    errors=Trip.objects.trip_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value,extra_tags =key)
        return redirect('/travels/add')
    else:
        user=User.objects.get(id=request.session['user'])
        dest=f"{request.POST['dest']}"
        desc=f"{request.POST['desc']}"
        trip=Trip.objects.create(destination=dest,description=desc,start=request.POST['start'],end=request.POST['end'])
        trip.travelers.add(user)
        return redirect('/travels')
def join_trip(request,num):
    number=int(num)
    user=User.objects.get(id=request.session['user'])
    trip=Trip.objects.get(id=number)
    trip.travelers.add(user)
    return redirect('/travels')

def trip(request,num):
    number=int(num)
    trip=Trip.objects.get(id=number)
    
    context={
        "trip":trip,
        "travelers":trip.travelers.values("name"),
        }
    return render(request,'app_one/destination.html',context)
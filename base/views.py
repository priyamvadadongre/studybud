from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,User
from .forms import RoomForm
from django.contrib import messages
# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try :
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user does not exist")

        user=authenticate(request,username=username,password=password)
        print(request)
        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request,"username or password does not exist")
    context={}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect("home") 
def home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
            ) # we use contains like the grep empty string is part of all topics
# i referes to case sensitive   
    room_count=rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms,"topics":topics,"room_count":room_count}
    return render(request,'base/home.html',context)


def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request,'base/room.html',context)

@login_required(login_url="/login")
def createRoom(request):
    form =RoomForm()
    if request.method=="POST":
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={"form":form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    # to get the data prefilled with old values we use instance
    form =RoomForm(instance=room)
    if request.method=="POST":
        form= RoomForm(request.POST,instance=room) # instance to show which room is being updated or else it'll create a new room 
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context={"form":form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    if request.user != room.host:
        return HttpResponse("you are not allowed here")
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':room})

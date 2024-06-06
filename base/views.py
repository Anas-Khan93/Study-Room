from django.shortcuts import render, redirect
# this q import will add AND and OR statements in the search bar in nav.html
from django.db.models import Q

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.contrib import messages

#from django.contrib.auth.models import User

#import the user model
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.forms import UserCreationForm

#first we import the model that we want to query
from .models import Room, Topic, Message,User

from .forms import RoomForm,UserForm, MyUserCreationForm


# Create your views here.

# we create our rooms which is basically a list of dictionaries or they represent objects
#rooms = [
#    {'id': 1, 'name': 'Lets learn python'},
#    {'id': 2, 'name': 'Design with me'},
#    {'id': 3, 'name': 'Frontend Developers'},

#]
# LOGIN PAGE
def loginPage(request):

    page = 'login'

    #basically if the user is authenticated we don't want him to relogin    
    if request.user.is_authenticated:
        return redirect('home')
    #that means the user entered his position
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email= email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email or Password does not exist')

    context= {'page':page}
    return render(request, 'base/login_register.html', context)


# LOGOUT FUNCTION:
def logoutUser(request):

    logout(request)
    return redirect('home')

# REGISTER FUNCTION
def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form':form})


# we return the rooms whenever our home tab or room tab is called
# HOME FUNCTION
def home(request):
    # we have a model manager. we can make queries by going into to the models
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # icontains before Topic__name__ means that whatever value we have in topic name atleast contains what's in here/
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # Limit the number of topics listed in the home page to 5   
    topics = Topic.objects.all().order_by('name')[:5]

    # for the number of rooms
    room_count = rooms.count()

    room_messages = Message.objects.filter(room__topic__name__icontains=q)

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request,'base/home.html', context)


# we are going to use the pk key to create a database
# ROOM FUNCTION
def room(request, pk):
    room = Room.objects.get(id=pk)

    # room.message_set.all() basically says give us the set of messages that are related to this room
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            # we pass in body from the room.html
            body = request.POST.get('body')

        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages':room_messages, 'participants':participants}

    return render(request, 'base/room.html', context )


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context= {'user': user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request,'base/profile.html', context)


@login_required(login_url= 'login')
def createRoom(request):
    form = RoomForm()
    #added later on for room template after we used new theme
    topics = Topic.objects.all()

    form = RoomForm(request.POST)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic= topic,
            name= request.POST.get('name'),
            description =request.POST.get('description'),
        )
        return redirect ('home')
        # fills the form with the POST data
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect ('home')
    
    context = {'form':form, 'topics':topics} 
    return render (request, 'base/room_form.html', context)


# we pass in the request and pass in the key to know what item we are updating
@login_required(login_url= 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    # This form will be prefilled with the above room value 
    form = RoomForm(instance = room)

    topics= Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to do that action')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'room':room, 'topics':topics}
    return render(request, 'base/room_form.html', context)


# restricting access to this function to specific user
# function for deleting a room
@login_required(login_url= 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    #if the user that requested the action is not a user of the room, then we restrict his action and throw an HTTPresponse.
    if request.user != room.host:
        return HttpResponse('You are not allowed to do that action')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


#Function for delete message
@login_required(login_url= 'login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    #if the user that requested the action is not a user of the room, then we restrict his action and throw an HTTPresponse.
    if request.user != message.user:
        return HttpResponse('You are not allowed to do that action')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

#Function for Editing User profile
@login_required(login_url='login')

def updateUser (request):
    user= request.user

    form = UserForm(instance=user)
    # context=[]

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES ,instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})


def topicsPage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q).order_by('name')
    return render(request, 'base/topics.html',{'topics':topics})


def activityPage(request):
    room_messages= Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})
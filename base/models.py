from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True , null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null= True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# we wanna create a room first

#Each Topic(parent class) can have multiple Rooms (child class)
# the only thing the topic will have is its name which we shall limit to 200 characters and return it.
class Topic (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room (models.Model):
    # we are going to have different attributes
    # first attribute would be the user that is connected or host for now we shall comment it out
    host= models.ForeignKey(User, on_delete= models.SET_NULL, null=True)

    # by stting the on_delete to null we donot want the room to be deleted completely.
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    # .charfield is basically a text field and we in brackets we have to identify the type of attribute and what type of attribute
    # charfield takes in value or parameter of max_length, it is require for it
    name = models.CharField(max_length=200)

    # NULL is same as charfield except its gonna be bigger. null=TRUE means that the database can have an instance without description
    # having a value (by default it is set to FALSE meaning instance would not be created since description is empty/blank)
    # BLANK= TRUE means that when we run the save method i.e run a forum. That forum can also be empty.
    # This is for the save method. NULL is for database, BLANK is for 
    description = models.TextField(null=True, blank= True)

    # This variable will store all the patricipants/users active in a particular room. if you comment in the room then you are active user
    participants = models.ManyToManyField(User, related_name='participants', blank=True)

    # we no shall add an updated value, this would take a snapshot of anytime, where this model instance was updated. so anytime we 
    # run the save method to update this model. It will take a timestamp
    # auto_now TRUE basically means everytime save method is called, go ahead and take a timestamp.
    updated = models.DateTimeField (auto_now= True)
    # We also want to know when this was created. auto_now_add basically means it takes a snap only once when the instance is created
    created = models.DateTimeField (auto_now_add= True)
    
    class Meta:
        # the hyphen before update and create makes the newest item comes first and then updated one
        ordering = ['-updated', '-created']

    # we are going to create a string representation of this room

    def __str__(self):
        return self.name
    


# we are gonna create a new model which is gonna be for any comment or message someone leaves in a room

class Message(models.Model):
    # we begin by first specifying the user who wrote the message
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    # then we specify the room. using one to many relationship we access the parent class. 
    # reason we On_delete=models.CASCADE, is to say that once a room is deleted we also want to delete all the messages.
    # if we set on_delete to SET_NULL that means it will save all the msgs in the database even if the room is deleted
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    # we also ofcourse want the body i.e text of the message. we leave it empty to force the user to write a msg and not leave blank.
    body = models.TextField()

    # similar to partent class (i.e ROOM) we want to know the date it was created and the date time it was updated
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    # instead of having to repeat order_by('-created') for each message we simply do it in our class Message
    class Meta:
        # the hyphen before update and create makes the newest item comes first and then updated one
        ordering = ['-updated', '-created']


    # followed by creating a string function to return the values
    def __str__(self):
        # we return the text of the body and keep it at max upto 50 char which is only for a preview. the og text is not limited to it
        return self.body[0:50]
    

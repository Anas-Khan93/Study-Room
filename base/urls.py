# This is our URL file for a specific application"

from django.urls import path
from . import views

urlpatterns = [

    path ('login/', views.loginPage, name='login'),
    
    path ('logout/', views.logoutUser, name='logout'),

    path ('register/', views.registerPage, name='register' ),

    path('', views.home, name="home"),
    
    # now we pass a string object for our room ids to display
    path('room/<str:pk>/', views.room, name="room" ),

    # URL for user profile
    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    # URL for create-room
    path('create-room/', views.createRoom, name="create-room"),

    # URL for update  room. we also pass in an ID for the room to be updated
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),

    # URL for updating the user profile
    path('update-user/', views.updateUser, name='update-user' ),

    # URL for deleteing a room
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),

    # URL for deleting a message
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    # URL for topics page(mobile menu and more on home)
    path('topics/', views.topicsPage, name='topics'),

    # URL for messages
    path('activity/', views.activityPage, name='activity')


]
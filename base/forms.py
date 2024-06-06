from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email', 'password1', 'password2']



# we import our model form and our model ROOM
class RoomForm(ModelForm):
    
    class Meta:
        model = Room
               
        # __all basically means take all the editable fields from the class Room
        fields = '__all__'

        # but exclude the following
        exclude = ['host','participants']

class UserForm (ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username', 'email','bio']
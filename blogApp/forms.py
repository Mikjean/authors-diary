from django.forms import ModelForm, fields
from blogApp.models import Comments, Post
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm



class Commentform(ModelForm):
    class Meta():
        model = Comments
        fields = '__all__'

class createForm(ModelForm):
    class Meta():
        model = Post
        fields = '__all__'


class createUserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class loginUserForm(ModelForm):
    class Meta():
        model = User
        fields = [ 'username', 'password']
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description']
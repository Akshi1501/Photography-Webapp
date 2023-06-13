from dataclasses import field, fields
from multiprocessing import AuthenticationError
from pyexpat import model
from django import forms
from .models import Image
from django.contrib.auth.forms import User
from .models import Profile
from django.forms import ModelForm
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        labels = {'photo':''} 
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


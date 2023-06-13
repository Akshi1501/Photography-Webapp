from unicodedata import name
from django.db import models
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import User
class Image(models.Model):
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(auto_now_add=True)

class con(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    desc = models.TextField()

class books(models.Model): 
    username = models.CharField(max_length=30)
    phone = models.CharField(max_length=10, null=True)
    eventname = models.CharField(max_length=30, null=True)
    date = models.DateTimeField(null=True, blank = True)
    descr = models.TextField(null=True)
    preferences=models.CharField(max_length=30, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile' 

class carts(models.Model):
    itemid = models.IntegerField()
    quantity = models.IntegerField()
    username = models.CharField(max_length=50)

class items(models.Model):
    itemid = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    descr = models.CharField(max_length=1000)
    image =  models.ImageField(upload_to="itemsimg")
    
class orders(models.Model):
    orderid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    primary_phone_no = models.CharField(max_length=50)
    secondary_phone_no = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    total_price = models.CharField(max_length=50)


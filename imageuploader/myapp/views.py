from datetime import date
from telnetlib import LOGOUT
from django.shortcuts import redirect, render
from .forms import ImageForm
from .models import *
from myapp.models import con
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def edit(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = ImageForm() 
    img = Image.objects.all()
    return render(request,'myapp/edit.html', {'img':img, 'form':form})

def home(request):
    return render(request,'myapp/main.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username already exixts, Choose a new one!')
            return redirect('signup')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Acoount successfully created, Please login")
        return redirect('signin')   
    return render(request,'myapp/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return redirect('home') 
        else:
            messages.error(request, "Incorrect Username or Password, try again!")
    return render(request, 'myapp/loginn.html')

def signout(request):
    logout(request)
    return redirect('signin')

def cont(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        desc = request.POST['desc']
        ins = con(name=name, email=email, phone=phone, desc=desc)
        ins.save()
        messages.success(request,'Your response has been submitted !!!')
    return render(request, "myapp/contactt.html") 

@login_required
def book(request):
        if request.method == "POST":
            username =request.POST['username']
            phone = request.POST['phone']
            eventname = request.POST['eventname']
            date = request.POST['date']
            if books.objects.filter(date=date).exists():
                messages.info(request, 'Date already booked, Pick another date')
                return redirect('book')     
            descr = request.POST['descr']
            preferences=request.POST['preferences']
            boo = books(username=username,phone=phone,descr=descr,preferences=preferences,eventname=eventname,date=date)
            boo.save()
            messages.success(request,'Your booking was successful!!!')
        return render(request, "myapp/bookings.html")  

def aboutus(request):
    return render(request, "myapp/aboutus.html")

@login_required
def profile(request):
    return render(request, "myapp/profile.html")
    
class DisplayBookings(LoginRequiredMixin, ListView):
    model = books
    template_name = "myapp/mybookings.html"
    context_object_name = 'bokk'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print ("self.request.user <<<< %s"%self.request.user)
        print ("context <<< %s"%context)
        data = []
        db_obj = books.objects.filter(username=self.request.user)
        for dat in db_obj:
            obj = {}
            obj['eventname'] = dat.eventname
            obj['date'] = dat.date.date
            obj['descr'] = dat.descr
            data.append(obj)
        print ("data <<<< %s"%data)
        context['bokk'] = data
        return context

def viewCart(request):
    context = {}
    all_items = items.objects.all()
    context['data'] = all_items
    return render(request, "myapp/cart.html", context)

def saveCart(request):
    itemid = request.POST.get('itemid')
    print ("itemid", itemid)
    user = request.user.username
    try:
        ex_objs = carts.objects.get(username=user, itemid=itemid)
    except:
        ex_objs = carts()
    ex_objs.username = user
    ex_objs.itemid = itemid
    if ex_objs.quantity:
        ex_objs.quantity += 1
    else:
        ex_objs.quantity = 1
    ex_objs.save()
    return viewCart(request)

def editCartItems(request):
    qty = request.POST.get('qty')
    itemid = request.POST.get('itemid')
    user = request.user.username
    ex_obj = carts.objects.get(itemid=itemid, username=user)
    ex_obj.quantity = int(qty)
    ex_obj.save()

def viewCartItems(request):
    itemid = request.POST.get('itemid')
    if itemid:
        editCartItems(request)
    context = {}
    all_cart_items = carts.objects.filter(username=request.user.username)
    all_item_id = list(map(lambda x : x.itemid, all_cart_items))
    all_item_info = items.objects.filter(itemid__in = all_item_id)
    item_count_map = {}
    for item in all_cart_items:
        item_count_map[item.itemid] = item.quantity
    for item in all_item_info:
        item.qty = item_count_map.get(item.itemid)
    context['data'] = all_item_info
    context['count_map'] = item_count_map
    return render(request, "myapp/viewcart.html", context)
    
def buyNow(request):
    user = request.user.username
    context = {}
    all_cart_items = carts.objects.filter(username=user)
    all_item_id = list(map(lambda x : x.itemid, all_cart_items))
    all_item_info = items.objects.filter(itemid__in = all_item_id)
    item_price_map = {}
    item_info = []
    total_price = 0
    for item in all_item_info:
        item_price_map[item.itemid] = item
    for item in all_cart_items:
        total_price += (item.quantity * float(item_price_map[item.itemid].price))
        info = {'item_name':item_price_map[item.itemid].name, 'quantity':item.quantity, 'image':item_price_map[item.itemid].image}
        item_info.append(info)
    context['total_price'] = total_price
    context['data'] = item_info
    return render(request, "myapp/buynow.html", context)

def placeOrder(request):
    user = request.user.username
    address = request.POST.get('address')
    primary_phone = request.POST.get('p_phone')
    sec_phone = request.POST.get('s_phone')
    pincode = request.POST.get('pin')
    total_price = request.POST.get('total_price')
    orders_obj = orders()
    orders_obj.username = user
    orders_obj.address = address
    orders_obj.primary_phone_no = primary_phone
    orders_obj.secondary_phone_no = sec_phone
    orders_obj.pincode = pincode
    orders_obj.total_price = total_price
    orders_obj.save()
    carts.objects.filter(username = user).delete()
    return render(request, "myapp/orderplaced.html", {'username':user})

def orderSummary(request):
    context = {}
    user = request.user.username
    orders_info = orders.objects.filter(username=user)
    context['data'] = orders_info
    return render(request, "myapp/order_summery.html", context)


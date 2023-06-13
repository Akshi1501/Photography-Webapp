from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from .views import DisplayBookings
from django.contrib import admin

admin.site.site_header = "PhotoArtistry Administration"

urlpatterns = [
    path('home', views.home, name="home"),
    path('', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('contact',views.cont,name="contact"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('edit',views.edit, name="edit"), 
    path('booking',views.book, name="book"),
    path('profile',views.profile, name="profile"),
    path('mybookings',DisplayBookings.as_view(), name='mybookings'), 
    path('cart',views.viewCart,name="cart"),
    path('saveCart',views.saveCart,name="save cart"),
    path('viewaddedcart',views.viewCartItems,name="view cart"),
    path('buynow',views.buyNow,name="Buy Now"),
    path('placeorder',views.placeOrder,name="Placeorder Now"),
    path('ordersummary',views.orderSummary,name="Order Summary"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

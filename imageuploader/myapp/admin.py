from django.contrib import admin
from .models import Image, books, Profile, carts, items, orders 
from .models import con
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'date']
class qq(admin.ModelAdmin):
    list_display = ['username', 'date','eventname']
class ww(admin.ModelAdmin):
    list_display = ['name']
class tt(admin.ModelAdmin):
    list_display = ['name','phone','desc']
class yy(admin.ModelAdmin):
    list_display = ['username','orderid','address','total_price']
admin.site.register(con,tt)
admin.site.register(books,qq)
admin.site.register(Profile)
admin.site.register(carts)
admin.site.register(items,ww)
admin.site.register(orders,yy)
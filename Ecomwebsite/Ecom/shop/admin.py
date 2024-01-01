from django.contrib import admin
from .models import *

class Product_Images(admin.TabularInline):
    model = Product_image
class Additional_Informations(admin.TabularInline):
    model = Additional_Information
class Product_admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)
    list_display = ('product_name', 'categories', 'section')
    list_editable = ('categories', 'section')

# Register your models here.
admin.site.register(Slider)
admin.site.register(banner_area)
admin.site.register(Main_category)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Product, Product_admin)
admin.site.register(Product_image)
admin.site.register(Additional_Information)
admin.site.register(Section)
admin.site.register(Avatar)
admin.site.register(Brand)
admin.site.register(Coupon_code)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(review)
class Review_Admin(admin.ModelAdmin):
    list_display = ('id','user','product' , 'price' ,'created_at','updated_at')
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User



# Create your models here.
class Slider(models.Model):
    DISCOUNT_DEALS = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels','New Arraivels'),
        ('New DEALS','New DEALS')
    )
    image = models.ImageField(upload_to='media/Slider_imgs')
    discount_deal = models.CharField(choices=DISCOUNT_DEALS,max_length=100)
    sale = models.IntegerField()
    Brand_name = models.CharField(max_length=200)
    discount = models.IntegerField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_name

class banner_area(models.Model):
    image = models.ImageField(upload_to='media/banner_imgs')
    discount_deal = models.CharField(max_length=100)
    quotes = models.CharField(max_length=100)
    discount = models.IntegerField()
    link = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.quotes

class Main_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Category(models.Model):
    main_category = models.ForeignKey(Main_category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name + "--" + self.main_category.name

class Sub_category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + "--" + self.category.name + "--" + self.name

class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_img = models.CharField(max_length=200)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField()
    Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    product_info = RichTextField()
    model_name = models.CharField(max_length=100)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    description = RichTextField()
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "shop_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)

class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    detail = models.CharField(max_length=100)

class Avatar(models.Model):
    imag1 = models.ImageField(upload_to='media/avatar_imgs')
    imag2 = models.ImageField(upload_to='media/avatar_imgs')
    imag3 = models.ImageField(upload_to='media/avatar_imgs')
    imag4 = models.ImageField(upload_to='media/avatar_imgs')
    imag5 = models.ImageField(upload_to='media/avatar_imgs')
    imag6 = models.ImageField(upload_to='media/avatar_imgs')
    imag7 = models.ImageField(upload_to='media/avatar_imgs')
    imag8 = models.ImageField(upload_to='media/avatar_imgs')

class Coupon_code(models.Model):
    code = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self):
        return self.code

class Order(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.fname, self.user)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{}'.format(self.order.id)
    
class review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    
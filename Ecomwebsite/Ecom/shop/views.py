from django.shortcuts import redirect,render
from .models import Slider,banner_area,Main_category,Product,Category,Brand,Coupon_code,Order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Max,Min,Sum
from cart.cart import Cart
import json
# Create your views here.

def main(request):
    Sliders = Slider.objects.all().order_by('-id')[0:3]
    banner = banner_area.objects.all().order_by('-id')[0:3]
    main_category = Main_category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name="Top Deals")
    print(product)
    context = {'sliders': Sliders, 'banner': banner, 'main_category': main_category, 'product': product}
    return render(request, 'main/main.html', context)


def PRODUCT_DETAIL(request,slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')
    context = {'product':product}
    return render(request,'product/product_detail.html',context)


def Error404(request):
    return render(request , 'errors/404.html')

def Login(request):
    return render(request , 'account/login.html')
def Signup(request):
    return render(request , 'account/signup.html')

def  LoggedIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('main')
        else:
            messages.error(request,'Email and password are Invalid !')
            return redirect('login')
    return redirect('login')

def REGISTER(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username = username).exists():
            messages.error(request,'Username already Exist !')
            return redirect('signup')
        if User.objects.filter(email = email).exists():
            messages.error(request,'This Email is already in use !')
            return redirect('signup')
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        messages.success(request,'Congratulations! you are registered successfully..')
        return redirect('signup')


@login_required(login_url='/shop/accounts/login/')
def profile_update(request):
    if request.method == 'POST':
        Fname = request.POST.get('Fname')
        Lname = request.POST.get('Lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user.first_name = Fname
        user.last_name = Lname
        user.email = email
        user.username = username
        user.save()
        messages.success(request,'Your Profile has been updated Successfully!')
        return redirect('profile')
    return render(request,'profile/profile.html')

@login_required(login_url='/shop/accounts/login/')
def PROFILE(request):
    return render(request,'profile/profile.html')


def About(request):
    return render(request,'main/about.html')


def Contact(request):
    return render(request,'main/contact.html')


def Product_view(request):
    category = Category.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
    else:
        product = Product.objects.all()
    context = {
        'category':category,
        'product':product,
        'min_p':min_price,
        'max_p':max_price,
        'FilterPrice':FilterPrice,
        'brand':brand
    }
    return render(request, 'main/product.html',context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    print(categories)
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()


    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})



@login_required(login_url="/shop/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("main")


@login_required(login_url="/shop/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/shop/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/shop/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/shop/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/shop/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    print(cart)
    coupon = None
    valid = None
    invalid = None
    if request.method == 'GET':
        code = request.GET.get('coupon_code')
        print(code)
        if code:
            try:
                coupon = Coupon_code.objects.get(code=code)
                valid = 'has been applied to your current order!'
            except:
                invalid = 'Invalid Coupon !!'

    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    context = {
        'pack':packing_cost,
        'tax':tax,
        'coupon':coupon,
        'valid':valid,
        'invalid':invalid
    }
    return render(request, 'cart/cart.html',context)
def checkout(request):
    coupon_discount = None
    if request.method == 'POST':
        coupon_discount = request.POST.get('coupon_discount')
        print("====" , coupon_discount)
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    tax_and_packing_cost = (packing_cost + tax)
    context = {
        'tax_and_packing_cost':tax_and_packing_cost,
        'coupon_discount':coupon_discount,
    }
    return render(request,'checkout/checkout.html',context)


def placeOrder(request):
    if request.method == 'POST':
        ord = Order()
        ord.user = request.user
        ord.fname = request.POST.get('first_name')
        ord.lname = request.POST.get('last_name')
        ord.city = request.POST.get('city')
        ord.address = request.POST.get('address')
        ord.state = request.POST.get('state')
        ord.pincode = request.POST.get('zip')
        ord.phone = request.POST.get('phone')
        ord.email = request.POST.get('email')
        id = request.user.id
        user = User.objects.get(id=id)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        ord.save()
        print('===========================================', ord.fname, ord.lname, ord.city, ord.address, ord.state,
              ord.pincode, ord.phone, ord.email)
        return redirect('main')
    return render(request,'order/order.html')

def rating(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.user.id)
        return None
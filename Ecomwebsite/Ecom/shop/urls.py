from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    #Error
    path('404',views.Error404,name='404'),

    path('', views.main,name='main'),
    path('product/<slug:slug>', views.PRODUCT_DETAIL, name='product_detail'),

    # Account

    path('Loggedin', views.LoggedIn, name='Loggedin'),
    path('login', views.Login, name='login'),
    path('About', views.About, name='About'),
    path('Contact', views.Contact, name='Contact'),
    path('Product', views.Product_view, name='Product'),
    path('filter-data',views.filter_data,name="filter-data"),
    path('register', views.REGISTER, name='handleregister'),
    path('signup', views.Signup, name='signup'),
    path('profile/', views.PROFILE, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('accounts/', include('django.contrib.auth.urls')),

    #cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'), 
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    #checkout
    path('cart/checkout/',views.checkout,name='checkout'),
    #placeOrder
    path('cart/placeOrder/',views.placeOrder,name='placeOrder'),
    #rating
    path('save/ratings',views.rating,name='rating')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
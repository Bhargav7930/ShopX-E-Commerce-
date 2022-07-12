from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('product/<slug>/',product_detail,name='product_detail'),
    path('login/',login_page,name='login_page'),
    path('register/',register_page,name='register_page'),
    path('error/',error_page),
    path('success/',success),
    path('token/',token_send),
    path('add-cart/<id>/',add_cart,name='add_cart'),
    path('show-cart/',show_cart,name='show_cart'),
    path('remove-cart/<id>/',remove_cart,name='remove_cart'),
    path('address/',ship_address,name='ship_address'),
    path('paymenthandler/',paymenthandler,name='payement'),
    path('checkout/',checkout,name='checkout'),
    path('search/',search,name='search'),
    path('logout/',logout_page,name='logout'),
    path('profile/',profile_page,name='profile'),
    path('change-password/',change_password,name='change_password'),
    path('delete-user/',delete_user,name='delete_user'),
    path('contact/',contact,name='contact'),

 
]

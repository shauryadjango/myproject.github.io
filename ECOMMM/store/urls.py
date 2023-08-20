from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('',views.RegisterForm,name='register'),
    path('login/',views.loginf,name='login'),
    path('logout/',views.logoutf,name='logout'),
]
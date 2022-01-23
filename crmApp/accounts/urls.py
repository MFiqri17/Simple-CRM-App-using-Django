from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="accounts-home"),
    path('customer/<pk>/', views.customer, name="accounts-customer"),
    path('products/', views.products, name="accounts-products"),
    path('create_order/<str:pk>/', views.CreateOrder, name="accounts-CreateOrder"),
    path('update_order/<str:pk>/', views.UpdateOrder, name="accounts-UpdateOrder"),
    path('delete_order/<str:pk>/', views.DeleteOrder, name="accounts-DeleteOrder"),
    path('register/', views.UserRegister, name="accounts-UserRegister"),
    path('login/', views.UserLogin, name="accounts-UserLogin"),
    path('logout/', views.userLogout, name="accounts-Logout"),
    path('user/', views.userPage, name="accounts-user"),
    path('account/', views.accountSettings, name="account"),

]


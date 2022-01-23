from django.db.models import fields
from django import forms
from django.forms import ModelForm, TextInput, PasswordInput
from django.forms import widgets
from django.forms.widgets import Select
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'status']
        widgets = {
            'product': TextInput(attrs={
                'class': "form-control"
            }),
            'status': Select(attrs={
                'class': "form-control"
            })
        }
        
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control"
            }),
            'email': TextInput(attrs={
                'class': "form-control"
            }),
            'password1': PasswordInput(attrs={
                'class': "form-control"
            }),
            'password2': PasswordInput(attrs={
                'class': "form-control"
            })
        }
        
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
                
            
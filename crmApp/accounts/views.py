from functools import total_ordering
import imp
from multiprocessing import allow_connection_pickling, context
from django.db.models import fields
from django.db.models.query import RawQuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, RegisterForm, CustomerForm
from django.forms import inlineformset_factory
from django.contrib import messages
from .filters import OrderFilter
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .decorators import unatuheticated_user, allowed_users, admin_only

from django.contrib.auth.models import Group

# Create your views here.
@login_required(login_url='accounts-UserLogin')
@admin_only
def home(request):
    
    ## Customer
    customer = Customer.objects.all().order_by('name')
    
    
    
    ## Order
    order = Order.objects.all().order_by('-date_created')
    total_order = order.count()
    delivered = order.filter(status="Delivered").count()
    pending = order.filter(status="Pending").count()
    
    context = {
        "customer": customer,
        "order": order,
        "total_order": total_order,
        "delivered":delivered,
        "pending":pending
    }

    return render(request, "accounts/dashboard.html", context)

@login_required(login_url='accounts-UserLogin')
def customer(request, pk):
    customer_id = Customer.objects.get(id = pk)
    # bisa dilakukan seperti ini
    # Orders = Order.objects.filter(customer=customer_id)
    Orders = customer_id.order_set.all()
    total_order = Orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=Orders)
    Orders = myFilter.qs
    
    context = {
        "customer_id":customer_id,
        "Orders":Orders,
        "total_order":total_order,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='accounts-UserLogin')
def products(request):
    products = Product.objects.all()
    context = {"products":products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='accounts-UserLogin')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id = pk)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    if request.method == "POST":
        # print("Printing Post: ", request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
            

    context = {'form':formset, 'customer':customer}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts-UserLogin')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"form":form, "order":order}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts-UserLogin')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request, pk):
    order = Order.objects.get(id = pk)
    order.delete()   
    return redirect('/')
    
    

@unatuheticated_user
def UserRegister(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('accounts-UserLogin')    
    
    context = {'form': form}
    
    return render(request, "accounts/register.html", context)


@unatuheticated_user
def UserLogin(request):   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        
        ## to check the user is already registered or not
        if user is not None:
            login(request, user)
            return redirect('accounts-home')
        
        else:
            messages.info(request, 'Username OR password is incorrect')
        
    context = {}
    return render(request, "accounts/login.html", context)

    
def userLogout(request):
    logout(request)
    return redirect('accounts-UserLogin') 

@login_required(login_url='accounts-UserLogin')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {'orders': orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)
  
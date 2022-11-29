from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):
    form= CreateUserForm()
    if request.method =="POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            username= form.cleaned_data.get('username')

            group = Group.objects.get(name= 'customer')
            user.groups.add(group)
            messages.success(request, "Account was created for" + username)
            return redirect('login')
    context= {'form': form}
    return render(request, 'register.html' ,context)

@unauthenticated_user
def loginPage(request):

    if request.method== "POST":
        username= request.POST.get("username")
        password= request.POST.get("password")

        user= authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.info(request, "Username OR password is wrong. Try Again.")
        

    context= { }
    return render(request, 'login.html' ,context)

def logoutUser(request):

    logout(request)
    return redirect("login")


@login_required(login_url= "login")
@admin_only
def home(request):
    orders= Order.objects.all()
    customers= Customer.objects.all()
    products= Product.objects.all()

    delivered= orders.filter(status= "Delivered").count()
    pending= orders.filter(status= "Pending").count()
    context= {'orders': orders, 'customers':customers, 'products':products,
    'pending': pending, 'delivered':delivered
    }

    return render(request, 'home.html' ,context)
    

def product(request):
    products= Product.objects.all()
    return render(request, 'product.html', {'products': products})

def customer(request):
    return render(request, 'customer.html')


@login_required(login_url= "login")
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form= OrderForm()
    if request.method== "POST":
        # print("Printing POST", request.POST)
        form= OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context=  {"form":form }
    return render(request, 'order_form.html', context)


@login_required(login_url= "login")
@admin_only
def updateOrder(request, pk):

    order= Order.objects.get(id=pk)
    form= OrderForm(instance=order)

    if request.method== "POST":
        form= OrderForm(request.POST,instance= order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context=  {"form":form }
    return render(request, 'order_form.html', context)


@login_required(login_url= "login")
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order= Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context= {'item':order}
    return render(request, 'delete.html', context)


@login_required(login_url= "login")
def userPage(request):
    context= {}
    return render(request, 'user.html', context)
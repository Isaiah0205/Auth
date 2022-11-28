from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *



def home(request):
    orders = Order.objects.all()
    customers = Customers.objects.all()
    context = {'orders': orders, 'customers': customers}
    return render(request, 'home.html', context)

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username/Password is incorrect.')
        context= {}
        return render(request, 'login.html', context)

def log_out(request):
    logout(request)
    return redirect('log_in')

def register(request):
    form = CreateUserForm(request.POST)

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account has been made for' +user)
            return redirect('log_in')
    context={'form': form}
    return render(request, 'register.html', context)
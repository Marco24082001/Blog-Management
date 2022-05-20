from email import message
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from blog_part.models import Blog
# Create your views here.

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Wrong credenticals")
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def registration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, 'Registration sucessful')
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)

def profile(request, pk):
    account = get_object_or_404(User, pk=pk)
    queryset = account.user_blog.all()
    blogs = queryset[:4]

    print(queryset)
    context = {
        'blogs': blogs,
        'account': account
    }
    return render(request, 'profile.html', context)


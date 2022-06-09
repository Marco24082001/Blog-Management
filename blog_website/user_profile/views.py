from email import message
from multiprocessing import context
import re
from urllib.request import Request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from blog_part.models import Blog
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *
from .decorators import (
    not_logged_in_required
)
# Create your views here.
@never_cache
@not_logged_in_required
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

@never_cache
@not_logged_in_required
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

@login_required(login_url='login')
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    form = UserProfileUpdateForm(instance=user)
    
    if request.method == "POST":
        if request.user.pk != user.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "user": user,
        "form": form
    }
    return render(request, 'profile.html', context)

@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            profile_image = request.FILES['profile_image']
            user = get_object_or_404(User, pk=request.user.pk)
            print(profile_image)
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = profile_image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('profile')

def user_information(request, username):
    if request.user.username == username:
        return redirect('profile')

    user = get_object_or_404(User, username = username)
    followers = user.followers.all()
    following = False
    if request.user.is_authenticated:
        if request.user in followers:
            following = True
    
    context = {
        'user': user,
        'followers': followers,
        'following': following,
    }
    return render(request, 'user_information.html', context)

@login_required(login_url = "login")
def follow_or_unfollow(request, user_id):
    followed = get_object_or_404(User, id=user_id)
    followed_by = get_object_or_404(User, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()

    return redirect("user_information", username=followed.username)
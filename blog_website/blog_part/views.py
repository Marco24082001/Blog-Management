from turtle import right
from unicodedata import category
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import *
# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-created_date')
    left_blog = blogs[0]
    center_blogs = blogs[1:4]
    right_blog = blogs[4]
    
    Lifestyle_blogs = blogs.filter(category__title__contains = 'LifeStyle')[:2]
    Fashion_blogs = blogs.filter(category__title__contains = 'Fashion')[:4]
    Travel_blogs = blogs.filter(category__title__contains = 'Travel')[:3]
    Technology_blogs = blogs.filter(category__title__contains = 'Technology')[:3]
    Food_blogs = blogs.filter(category__title__contains = 'Food & Drink')[:3]
    Health_blogs = blogs.filter(category__title__contains = 'Health Beauty')[:3]
    
    context =  {
        'left_blog': left_blog,
        'right_blog': right_blog,
        'center_blogs': center_blogs,
        'Lifestyle_blogs': Lifestyle_blogs,
        'Fashion_blogs': Fashion_blogs,
        'Travel_blogs': Travel_blogs,
        'Technology_blogs': Technology_blogs,
        'Food_blogs': Food_blogs,
        'Health_blogs': Health_blogs
    }

    return render(request, 'index.html', context)

def category_blog(request):
    return render(request, 'category_blog.html')

def blog_list(request):
    queryset = Blog.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    recent_blogs = queryset[:3]
    paginator = Paginator(queryset, 4)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blog')

    context = {
        'recent_blogs': recent_blogs,
        'blogs': blogs
    }
    return render(request, 'blog_list.html', context)
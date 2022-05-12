from unicodedata import category
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .models import *
# Create your views here.

def home(request):
    return render(request, 'index.html')

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
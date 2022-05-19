from turtle import right
from unicodedata import category
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic import DetailView
from .models import *
from .forms import *
from django.contrib import messages
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

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blog.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        'category': category.title,
        'blogs': blogs,
    }
    return render(request, 'category_blog.html', context)

def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        'tag': tag.title,
        'blogs': blogs,
    }
    return render(request, 'tag_blog.html', context)

def blog_list(request):
    queryset = Blog.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blog')

    context = {
        'blogs': blogs
    }
    return render(request, 'blog_list.html', context)

def search_blogs(request):
    search_key = request.GET.get('search', None)
    page = request.GET.get('page', 1)
    print(page)
    print(search_key)
    if search_key:
        queryset = Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key)
        ).distinct()

        paginator = Paginator(queryset, 6)
        try:
            blogs = paginator.page(page)
        except EmptyPage:
            blogs = paginator.page(1)
        except PageNotAnInteger:
            blogs = paginator.page(1)
            return redirect('home')

        context = {
            "blogs": blogs,
            "search_key": search_key
        }

        return render(request, 'search_blog.html', context)

    else:
        return redirect('home')

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'detail_blog.html'
    context_object_name = 'blog'
    # def get_object(self, query_set=None):
    #     return Blog.objects.get(slug=self.kwargs.get('slug'))

def create_blog(request):
    form = CreateBlogForm()
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category

            blog.save()
            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
            
            messages.success(request, "Blog added successfully")
            return redirect('blog_detail', slug=blog.slug)
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request, 'create_blog.html', context)
    
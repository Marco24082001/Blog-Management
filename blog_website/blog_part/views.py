from email import message
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic import DetailView
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    blogs = Blog.objects.order_by('-created_date')
    left_blog = blogs[0]
    center_blogs = blogs[1:4]
    right_blog = blogs[4]
    
    travel_blogs = blogs.filter(category__title__contains = 'Du lịch')
    technology_blogs = blogs.filter(category__title__contains = 'Công nghệ')
    education_blogs = blogs.filter(category__title__contains = 'Giáo dục')
    law_blogs = blogs.filter(category__title__contains = 'Pháp luật')
    world_blogs = blogs.filter(category__title__contains = 'Thế giới')
    
    context =  {
        'left_blog': left_blog,
        'right_blog': right_blog,
        'center_blogs': center_blogs,
        'travel_blogs': travel_blogs,
        'technology_blogs': technology_blogs,
        'education_blogs': education_blogs,
        'law_blogs': law_blogs,
        'world_blogs': world_blogs,
    }

    return render(request, 'index.html', context)

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.category_blogs.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 8)
    
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
    paginator = Paginator(queryset, 8)
    
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
    paginator = Paginator(queryset, 8)
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

@login_required(login_url='login')
def favorite_blog_list(request):
    queryset = Blog.objects.filter(user__user_followers__followed_by=request.user).order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 8)
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

        paginator = Paginator(queryset, 8)
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

def blog_detail(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    liked = request.user in blog.likes.all()


    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            print('thanhvi')
            print(form.cleaned_data.get('text'))
            Comment.objects.create( 
                user = request.user,
                blog = blog,
                text = form.cleaned_data.get('text')
            )
            return redirect(reverse('blog_detail', kwargs= {"slug": slug})+'#comments')
    else:
        blog.view += 1
        blog.save()

    context = {
        'blog' : blog,
        'form' : form,
        'liked' : liked
    }
    return render(request, 'detail_blog.html', context)

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

def detete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    pass

@login_required(login_url='login')
def my_blogs(request):
    queryset = request.user.user_blogs.all().order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 8)

    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk = delete)
        if request.user.pk != blog.user.pk:
            return redirect('home')
        blog.delete()
        messages.success(request, 'Your blog has been deleted !')
        return redirect('my_blogs')
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        'blogs' : blogs,
    }
    return render(request, 'my_blogs.html', context)
    
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = CreateBlogForm(instance=blog)
    tags = ','.join([tag.title for tag in blog.tags.all()])
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES, instance=blog)
        
        if form.is_valid():
            
            if request.user.pk != blog.user.pk:
                return redirect('home')

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

            messages.success(request, "Blog updated successfully")
            return redirect('blog_detail', slug=blog.slug)
        else:
            print(form.errors)


    context = {
        "form": form,
        "blog": blog,
        "tags": tags
    }
    return render(request, 'update_blog.html', context)


@login_required(login_url='login')
def add_reply(request, slug, comment_id):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user = request.user,
                comment = comment,
                text = form.cleaned_data.get('text')
            )
            return redirect(reverse('blog_detail', kwargs= {'slug': slug})+'#comments')

@login_required(login_url='login')
def like_blog(request, pk):
    context = {}
    blog = get_object_or_404(Blog, pk=pk)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()

    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()
    
    return JsonResponse(context, safe=False)


def report_blog(request, slug):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cate = request.POST['catereport']
            nd = request.POST['message']
            rp = Report(
                user = request.user,
                blog = Blog.objects.get(slug = slug),
                category = CateReport.objects.get(id = cate),
                message = nd
            )
            rp.save()
            return redirect(reverse('blog_detail', kwargs= {"slug": slug}))
            # return HttpResponse(f'ddax to cao {slug}, {cate}, {nd}')
    context =  {
        'tf' : form,
        'slug': slug
    }
    return render(request, 'report.html', context)
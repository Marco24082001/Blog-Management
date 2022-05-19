from multiprocessing import context
from .models import *

def get_context_variable(request):
    categories = Category.objects.all()
    recent_blogs = Blog.objects.order_by('-created_date')[:3]
    popular_blogs = Blog.objects.order_by('-likes')[:3]
    context = {
        'categories': categories,
        'recent_blogs': recent_blogs,
        'popular_blogs': popular_blogs
    }
    return context
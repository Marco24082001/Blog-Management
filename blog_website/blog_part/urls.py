from django.urls import URLPattern, path
# from jmespath import search
from .views import *


urlpatterns = [
    path('', home, name=''),
    path('category', category_blog, name='category'),
    path('blog_list', blog_list, name='blog_list'),
]
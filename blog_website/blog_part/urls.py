from django.urls import URLPattern, path
# from jmespath import search
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('category/<str:slug>/', category_blogs, name='category'),
    path('tag/<str:slug>/', tag_blogs, name='tag'),
    path('blog_list', blog_list, name='blog_list'),
    path('search', search_blogs, name='search'),
    path('blog/detail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create', create_blog, name='create_blog'),
]
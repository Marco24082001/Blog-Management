from django.urls import URLPattern, path
# from jmespath import search
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('category/<str:slug>/', category_blogs, name='category'),
    path('tag/<str:slug>/', tag_blogs, name='tag'),
    path('blog_list', blog_list, name='blog_list'),
    path('favorite_blog_list', favorite_blog_list, name='favorite_blog_list'),
    path('search', search_blogs, name='search'),
    # path('blog/detail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/detail/<slug:slug>/', blog_detail, name='blog_detail'),
    # path('blogs/<int:pk>', my_blog, name='my_blogs'),
    path('my_blogs', my_blogs, name='my_blogs'),
    path('blog/create', create_blog, name='create_blog'),
    path('blog/update/<slug:slug>', update_blog, name='update_blog'),
    path('blogs/delete/<int:pk>', detete_blog, name='delete_blog'),
    path('add_reply/<slug:slug>/<int:comment_id>', add_reply, name='add_reply'),
    path('like_blog/<int:pk>', like_blog, name='like_blog'),
    path('report/<str:slug>/', report_blog, name='report_blog'),
]
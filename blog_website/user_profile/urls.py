from django.urls import URLPattern, path

from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
    path('user_information/<str:username>/', user_information, name='user_information'),
    path('follow_or_unfollow/<int:user_id>/', follow_or_unfollow, name='follow_or_unfollow'),
]

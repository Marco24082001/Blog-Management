from django.urls import URLPattern, path
# from jmespath import search
from .views import *


urlpatterns = [
    path('', home, name=''),
]
from django.urls import path
from .views import principal

urlpatterns = [
    path('main/', principal, name='pablofederico'),
]
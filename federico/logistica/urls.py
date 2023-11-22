from django.urls import path
from . import views

urlpatterns = [path('logistica_main', views.logistica_main, name='logistica_main'),
                path('logistica_crear', views.logistica_crear, name='logistica_crear'),
]
from django.urls import path
from . import views

urlpatterns = [path('main_disponibilidad', views.main_disponibilidad, name='main_disponibilidad'),
               path('mostrar_disponibilidad/<int:anio>/<str:mes>/', views.mostrar_disponibilidad, name='mostrar_disponibilidad'),
               path('cargo_disponibilidad', views.cargo_disponibilidad, name='cargo_disponibilidad'),
               ]

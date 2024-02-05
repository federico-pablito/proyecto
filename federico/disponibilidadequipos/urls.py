from django.urls import path
from . import views

urlpatterns = [path('', views.main_disponibilidad, name='main_disponibilidad'),
               path('<int:anio>/<str:mes>', views.mostrar_disponibilidad, name='mostrar_disponibilidad'),
               path('cargar', views.cargo_disponibilidad, name='cargo_disponibilidad'),
               ]

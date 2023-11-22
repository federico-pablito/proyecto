from django.urls import path
from .views import reparaciones_main, reparaciones_crear, reparaciones_editar
urlpatterns = [
    path('reparaciones_main', reparaciones_main, name='reparaciones-main'),
    path('reparaciones_crear', reparaciones_crear, name='reparaciones-crear'),
    path('reparaciones_editar/<int:id>', reparaciones_editar, name='reparaciones-editar'),
]
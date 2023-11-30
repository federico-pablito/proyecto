from django.urls import path
from . import views

urlpatterns = [
    path('partesdiario_main', views.partesdiario_main, name='partesdiario_main'),
    path('partediario_editar/<int:id>/', views.partediario_editar, name='partediario_editar'),
    path('partediario_crear', views.partediario_crear, name='partediario_crear'),
    path('partes_pd_view', views.partes_pd_view.as_view(), name='partes_pd_view'),
]
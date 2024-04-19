from django.urls import path
from . import views

urlpatterns = [path('cargar_proveedor/', views.cargar_proveedor, name='cargar_proveedor'),
               path('cargar_evaluacion/', views.cargar_evaluacion, name='cargar_evaluacion'),
               path('', views.main_evaluacion, name='main_evaluacion'),
               path('informe_proveedor/<int:id_proveedor>', views.informe_proveedor, name='informe_proveedor')
               ]

from django.urls import path
from . import views

urlpatterns = [path('cargar', views.cargar_reparacion, name='cargar_reparacion'),
               path('', views.reparaciones_main, name='reparaciones-main'),
               path('editar/<int:id>', views.reparaciones_editar, name='reparaciones_editar'),
               path('<str:interno>', views.reparaciones_info, name='reparaciones_info'),
               path('cambiar_estado/<int:id>', views.cambiar_estado, name='cambiar_estado_rep')
               ]

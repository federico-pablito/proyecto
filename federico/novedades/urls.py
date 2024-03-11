from django.urls import path
from . import views

urlpatterns = [path('', views.novedades_main, name='novedades_main'),
               path('cargar', views.novedades_crear, name='novedades_crear'),
               path('<str:interno>', views.novedades_info, name='novedades_info'),
               path('cargar/<str:interno>', views.novedades_specifica_crear, name='novedades_specifica_crear'),
               path('cambiar_estado/<int:id>', views.cambiar_estado, name='cambiar_estado'),
               path('detalle/<int:id>', views.novedades_detalle, name='novedades_detalle'),
               path('exportar/', views.exportar_novedades, name='exportar_novedades'),
               ]

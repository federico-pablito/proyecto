from django.urls import path
from . import views

urlpatterns = [path('', views.logistica_main, name='logistica_main'),
               path('cargar', views.logistica_crear, name='logistica_crear'),
               path('editar/<int:id>/', views.logistica_editar, name='logistica_editar'),
               path('pdf', views.logistica_pdf, name='logistica_pdf_view'),
               path('requerimiento/equipo/cargar', views.requerimiento_equipo_crear, name='requerimiento_equipo_crear'),
               path('requerimiento/traslado/cargar', views.requerimiento_traslado_crear, name='requerimiento_traslado_crear'),
               path('cronograma/crear', views.cronograma_crear, name='cronograma_crear'),
               path('requerimiento/equipo', views.requerimiento_equipo_mostrar, name='requerimiento_equipo_mostrar'),
               path('requerimiento/traslado', views.requerimiento_traslado_mostrar, name='requerimiento_traslado_mostrar'),
               path('cronograma', views.cronograma_mostrar, name='cronograma_mostrar'),
               path('requerimiento/equipo/<int:id>', views.requerimiento_equipo_info, name='requerimiento_equipo_info'),
               path('requerimiento/traslado/<int:id>', views.requerimiento_traslado_info, name='requerimiento_traslado_info'),
               path('requerimiento/traslado/aprobar/<int:id>', views.requerimiento_traslado_aprobar, name='requerimiento_traslado_aprobar'),
               path('requerimiento/equipo/aprobar/<int:id>', views.requerimiento_equipo_aprobar, name='requerimiento_equipo_aprobar'),
               ]

from django.urls import path
from . import views
urlpatterns = [
    path('', views.reparaciones_main, name='reparaciones-main'),
    path('cargar', views.reparaciones_crear, name='reparaciones-crear'),
    path('editar/<int:id>', views.reparaciones_editar, name='reparaciones_editar'),
    path('pdf', views.reparaciones_pdf, name='reparaciones_pd_view'),
    path('<str:interno>', views.reparaciones_info, name='reparaciones_info'),
]
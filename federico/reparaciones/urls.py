from django.urls import path
from . import views
urlpatterns = [
    path('reparaciones_main', views.reparaciones_main, name='reparaciones-main'),
    path('reparaciones_crear', views.reparaciones_crear, name='reparaciones-crear'),
    path('reparaciones_editar/<int:id>', views.reparaciones_editar, name='reparaciones_editar'),
    path('reparaciones_pdf', views.reparaciones_pdf, name='reparaciones_pd_view'),
    path('<str:interno>', views.reparaciones_info, name='reparaciones_info'),
]
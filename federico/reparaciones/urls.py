from django.urls import path
from . import views
urlpatterns = [
    path('reparaciones_main', views.reparaciones_main, name='reparaciones-main'),
    path('reparaciones_crear', views.reparaciones_crear, name='reparaciones-crear'),
    path('reparaciones_editar/<int:id>', views.reparaciones_editar, name='service_editar'),
    path('reparaciones_pd_view', views.reparaciones_pd_view.as_view(), name='reparaciones_pd_view')
]
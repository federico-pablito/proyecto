from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_main, name='serviceprin'),
    path('editar/<str:interno>', views.editar_serv, name='editar_serv'),
    path('cargar/<str:interno>', views.crear_serv, name='create-serv'),
    path('pdf', views.services_pdf, name='services_pd_view'),
    path('<str:interno>/', views.info_serv, name='info_serv'),
    path('exportar', views.exportar_services, name='exportar_services'),
    path('exportar_normales', views.exportar_normales, name='exportar_normales'),
    path('exportar_proximos', views.exportar_proximos, name='exportar_proximos'),
    path('exportar_necesitan', views.exportar_necesitan, name='exportar_necesitan'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('mainservice', views.service_main, name='serviceprin'),
    path('editarserv/<str:interno>/', views.editar_serv, name='editar_serv'),
    path('create_serv', views.crear_serv, name='create-serv'),
    path('services_pd_view', views.services_pd_view.as_view(), name='services_pd_view'),
    path('info_serv/<str:interno>/', views.info_serv, name='info_serv'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('mainservice', views.service_main, name='serviceprin'),
    path('editarserv/<int:id>/', views.editar_serv, name='editar_serv'),
    path('create_serv', views.crear_serv, name='create-serv'),
    path('internos_pd_view', views.internos_pd_view.as_view(), name='internos_pd_view'),
]
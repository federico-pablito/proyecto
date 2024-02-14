from django.urls import path
from . import views

urlpatterns = [
    path('', views.tanque_detail, name='detalleTanque'),
    path('actualizartanques/', views.actualizar_tanques, name='javaactualizar'),
    path('registrar_consumo/', views.registrar_consumo, name='registrarConsumo'),
    path('registrar_repostaje/', views.registrar_repostaje, name='repostaje'),
    path('historialCargas', views.historial_cargas, name='registrarCarga'),
    path('historialRepostaje', views.historial_repostajes, name='registarRepostaje'),
]

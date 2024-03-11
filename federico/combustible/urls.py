from django.urls import path
from . import views

urlpatterns = [
    path('', views.tanque_detail, name='detalleTanque'),
    path('actualizartanques/', views.actualizar_tanques, name='javaactualizar'),
    path('consumo/', views.registrar_consumo, name='registrarConsumo'),
    path('repostaje/', views.registrar_repostaje, name='repostaje'),
    path('consumos', views.historial_cargas, name='registrarCarga'),
    path('repostajes', views.historial_repostajes, name='registarRepostaje'),
    path('exportar_consumos/', views.exportar_consumos, name='exportar_consumos'),
    path('exportar_repostajes/', views.exportar_repostajes, name='exportar_repostajes'),
]

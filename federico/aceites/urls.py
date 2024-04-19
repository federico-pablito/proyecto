from django.urls import path
from . import views

urlpatterns = [
    path('', views.aceite_detail, name='detalleAceite'),
    path('actualizarAceites/', views.actualizar_aceites, name='actualizaraceites'),
    path('consumo/', views.registrar_consumo_aceite, name='realizarcarga'),
    path('repostar/', views.registrar_repostaje_aceite, name='realizarrepostaje'),
    path('repostaje/', views.historial_repostaje_aceite, name='historialaceite'),
    path('consumos/', views.historial_consumos_aceite, name='historialconsumoaceite'),
    path('exportar_consumos/', views.exportar_consumos_aceite, name='exportar_consumos_aceite'),
    path('exportar_repostajes/', views.exportar_repostajes_aceite, name='exportar_repostajes_aceite'),
]

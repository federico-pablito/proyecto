from django.urls import path
from . import views

urlpatterns = [
    path('', views.aceite_detail, name='detalleAceite'),
    path('actualizaaceites/', views.actualizar_aceites, name='actualizaraceites'),
    path('cargaaceite/', views.registrar_consumo_aceite, name='realizarcarga'),
    path('registrarrepostaje/', views.registrar_repostaje_aceite, name='realizarrepostaje'),
    path('aceiterepostado/', views.historial_repostaje_aceite, name='historialaceite'),
    path('historialconsumoaceites/', views.historial_consumos_aceite, name='historialconsumoaceite'),

]
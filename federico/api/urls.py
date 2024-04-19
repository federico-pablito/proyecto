from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('reparaciones/', ReparacionList.as_view(), name='reparacion-list'),
    path('ordenes/', OrdenReparacionList.as_view(), name='orden-list'),
    path('ordenes_items/', OrdenReparacionItemList.as_view(), name='orden_item-list'),
    path('supervisores/', SupervisorList.as_view(), name='supervisor-list'),
    path('talleres/', TallerList.as_view(), name='taller-list'),
    path('mecanicos_encargados/', MecanicoEncargadoList.as_view(), name='mecanico-list'),
    path('internos/', InternosList.as_view(), name='interno-list'),
    path('services/', ServiceList.as_view(), name='service-list'),
    path('novedades/', NovedadList.as_view(), name='novedad-list'),
    path('unidadesdeproduccion/', UPList.as_view(), name='up-list'),
    path('choferes/', ChoferList.as_view(), name='chofer-list'),
    path('operadores/', OperadorList.as_view(), name='operador-list'),
    #Ver como hacer disponibilidad de equipos
    #path('disponibilidad/', DisponibilidadList.as_view(), name='disponibilidad-list'),
    path('tiposactividad/', TipoActividadList.as_view(), name='tipoactividad-list'),
    #Alquileres de equipos
    #path('alquileres/', AlquilerList.as_view(), name='alquiler-list'),
    #certificados tambien
    #path('certificados/', CertificadoList.as_view(), name='certificado-list'),
    path('tiposvehiculos/', TipoVehiculoList.as_view(), name='tipovehiculo-list'),
    path('urgencias/', UrgenciaList.as_view(), name='urgencia-list'),
    path('filtro_internos/', FiltroInternosList.as_view(), name='filtro-internos'),
    path('neumaticos_internos/', NeumaticoInternosList.as_view(), name='neumaticos-internos'),
    path('tanques/', TanqueList.as_view(), name='tanque-list'),
    path('consumos/', ConsumoList.as_view(), name='consumo-list'),
    path('repostajes/', RepostajeList.as_view(), name='repostaje-list'),
    path('tanques_aceite/', TanqueAceiteList.as_view(), name='tanque_aceite-list'),
    path('consumos_aceite/', ConsumoAceiteList.as_view(), name='consumo_aceite-list'),
    path('repostajes_aceite/', RepostajeAceiteList.as_view(), name='repostaje_aceite-list'),

]
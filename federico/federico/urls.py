from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import reparaciones



urlpatterns = [
    path('configuraciones/', admin.site.urls),
    path('', include('login.urls')),
    path('main/', include('main.urls')),
    path('maestroequipo/', include('maestroequipos.urls')),
    path('service/', include('service.urls')),
    path('unidadesproduccion/', include('unidadesproduccion.urls')),
    path('maininicio/', include('login.urls')),
    path('disponibilidadequipos/', include('disponibilidadequipos.urls')),
    path('novedades/', include('novedades.urls')),
    path('combustible/', include('combustible.urls')),
    path('aceites/', include('aceites.urls')),
    path('reparaciones/', include('reparaciones.urls')),
    path('cargar_orden', reparaciones.views.crear_orden, name='crear_orden'),
    path('ordenes', reparaciones.views.main_ordenes, name='ordenes'),
    path('parte_mecanicos', reparaciones.views.main_parte_mecanicos, name='main_parte_mecanicos'),
    path('cargar_parte/', reparaciones.views.cargar_parte_mecanicos, name='cargar_parte_mecanicos'),
    path('api/', include('api.urls')),
    path('logistica/', include('logisticas.urls')),
    path('proveedores/', include('proveedores.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

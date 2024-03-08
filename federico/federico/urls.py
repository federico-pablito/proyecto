from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import reparaciones



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('main/', include('main.urls')),
    path('maestroequipo/', include('maestroequipos.urls')),
    path('service/', include('service.urls')),
    path('unidadesproduccion/', include('unidadesproduccion.urls')),
    path('logistica/', include('logistica.urls')),
    path('maininicio/', include('login.urls')),
    path('disponibilidadequipos/', include('disponibilidadequipos.urls')),
    path('novedades/', include('novedades.urls')),
    path('combustible/', include('combustible.urls')),
    path('aceites/', include('aceites.urls')),
    path('reparaciones/', include('reparaciones.urls')),
    path('cargar_orden', reparaciones.views.crear_orden, name='crear_orden'),
    path('ordenes', reparaciones.views.main_ordenes, name='ordenes'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

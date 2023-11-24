
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('maestroequipo/', include('maestroequipos.urls')),
    path('service/', include('service.urls')),
    path('unidadesproduccion/', include('unidadesproduccion.urls')),
    path('tablamadre/', include('tablamadre.urls')),
    path('reparaciones/', include('reparaciones.urls')),
    path('logistica/', include('logistica.urls')),
    path('partesdiarios/', include('partesdiarios.urls')),
    path('maininicio/', include('login.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
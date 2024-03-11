from django.urls import path
from . import views

urlpatterns = [
    path('', views.verunidadproduccion, name='visualizar_ups'),
    path('pdf', views.unidades_pdf_view.as_view(), name='unidades_pdf_view'),
    path('exportar', views.exportar_ups, name='exportar_ups')
]
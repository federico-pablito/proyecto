from django.urls import path
from . import views

urlpatterns = [
    path('visualizar_ups', views.verunidadproduccion, name='visualizar_ups'),
    path('unidades_pdf_view', views.unidades_pdf_view.as_view(), name='unidades_pdf_view')
]
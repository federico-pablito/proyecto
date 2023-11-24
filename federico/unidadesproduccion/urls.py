from django.urls import path
from .views import verunidadproduccion, unidades_pdf_view

urlpatterns = [
    path('visualizar_ups', verunidadproduccion, name='visualizar_ups'),
    path('unidades_pdf_view', unidades_pdf_view.as_view(), name='unidades_pdf_view')
]
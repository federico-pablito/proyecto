from django.urls import path
from .views import verunidadproduccion

urlpatterns = [
    path('visualizar_ups', verunidadproduccion, name='visualizar_ups')
]
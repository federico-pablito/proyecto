from django.urls import path
from . import views

urlpatterns = [
    path('', views.solicitar_traslado, name='solicitudtraslado'),
    path('aprobar/<int:traslado_id>/', views.aprobar_traslado, name='aprobar_traslado')
]

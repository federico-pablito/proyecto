from django.urls import path
from . import views

urlpatterns = [
    path('mostrartablamadres', views.mostrartablamadre, name='mostrartablamadres'),
]
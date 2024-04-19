from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChooseForm, name='choose_form'),  
    path('ver/', views.VerForms, name='ver_forms'), 
    path('ver_form_detalle/<int:form_id>/', views.VerDetalle, name='ver_form_detalle'),  
    path('completar/<str:form_type>/', views.CompletarFormulario, name='completar_formulario'),  # Ajuste aquí
    path('solicitar_logistica/', views.SolicitarTraslado, name='solicitar_logistica'),
    path('ver_solicitudes/', views.VerSolicitudes, name='ver_solicitudes'),
]

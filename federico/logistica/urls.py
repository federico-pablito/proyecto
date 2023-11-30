from django.urls import path
from . import views

urlpatterns = [path('logistica_main', views.logistica_main, name='logistica_main'),
                path('logistica_crear', views.logistica_crear, name='logistica_crear'),
                path('logistica_editar', views.logistica_editar, name='logistica_editar'),
                path('logistica_pdf_view', views.logistica_pdf_view.as_view(), name='logistica_pdf_view'),
]
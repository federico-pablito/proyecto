from django.urls import path
from . import views

urlpatterns = [path('cargar', views.cargointerno, name='cargointernos'),
               path('editar/<int:id>/', views.editar_interno, name='editar_interno'),
               path('', views.mainmaestroequipos, name='main-maestroequipos'),
               path('alquileres', views.alquileresinternos, name='alquileresinternos'),
               path('alquilerequipo', views.alquilerequipo, name='alquilerequipo'),
               path('info/<int:id>/', views.info_interno, name='info_interno'),
               path('certificado/<int:id>/<str:mesanio>', views.certificado_equipoalquilado, name='certificado_equipoalquilado'),
               path('pdf/<str:form_values>/', views.generate_pdf_view, name='generate_pdf_view'),]

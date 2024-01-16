from django.urls import path
from . import views

urlpatterns = [path('filtrointernos', views.filtrointernos, name='filtrointernos'),
               path('cargointerno', views.cargointerno, name='cargointernos'),
               path('editar_interno/<int:id>/', views.editar_interno, name='editar_interno'),
               path('mainmaestro', views.mainmaestroequipos, name='main-maestroequipos'),
               path('alquileresinternos', views.alquileresinternos, name='alquileresinternos'),
               path('alquilerequipo', views.alquilerequipo, name='alquilerequipo'),
               path('info_interno/<int:id>/', views.info_interno, name='info_interno'),
               path('certificado_equipoalquilado/<int:id>/<str:mesanio>', views.certificado_equipoalquilado, name='certificado_equipoalquilado'),
               path('generate_pdf_view/<str:form_values>/', views.generate_pdf_view, name='generate_pdf_view'),]

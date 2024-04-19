from django.urls import path
from . import views

urlpatterns = [path('cargar', views.cargointerno, name='cargointernos'),
               path('editar/<int:id>/', views.editar_interno, name='editar_interno'),
               path('', views.mainmaestroequipos, name='main-maestroequipos'),
               path('alquileres', views.alquileresinternos, name='alquileresinternos'),
               path('alquilerequipo', views.alquilerequipo, name='alquilerequipo'),
               path('info/<int:id>/', views.info_interno, name='info_interno'),
               path('certificado/<int:id>/<str:mesanio>', views.certificado_equipoalquilado, name='certificado_equipoalquilado'),
               path('cargar_filtro/<str:interno>', views.cargo_filtros, name='cargo_filtros'),
               path('filtro/<str:interno>/', views.mostrar_filtros, name='mostrar_filtros'),
               path('cargar_neumatico/<str:interno>/', views.cargo_neumaticos, name='cargo_neumaticos'),
               path('neumatico/<str:interno>/', views.mostrar_neumaticos, name='mostrar_neumaticos'),
               path('exportar_internos', views.exportar_internos, name='exportar_internos'),
               path('cargar_chofer', views.cargar_chofer, name='cargar_chofer'),
               path('cargar_operador', views.cargar_operario, name='cargar_operario'),
               path('operadores', views.main_operadores, name='main_operadores'),
               path('choferes', views.main_choferes, name='main_choferes'),
               path('cargar_fotos', views.cargar_fotos, name='cargar_fotos'),
               path('cargar_adjuntos', views.cargar_adjuntos, name='cargar_adjuntos'),
               path('adjuntos/<int:id>', views.ver_adjuntos, name='main_adjuntos'),
               ]

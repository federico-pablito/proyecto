from django.urls import path
from . import views

urlpatterns = [path('filtrointernos', views.filtrointernos, name='filtrointernos'),
               path('cargointerno', views.cargointerno, name='cargointernos'),
               path('editar_interno/<int:id>/', views.editar_interno, name='editar_interno'),
               path('mainmaestro', views.mainmaestroequipos, name='main-maestroequipos'),
               path('internos_pd_view', views.internos_pd_view.as_view(), name='internos_pd_view'),]

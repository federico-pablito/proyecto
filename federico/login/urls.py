from django.urls import path
from .views import inicio_view

urlpatterns = [
    # Otras URL de tu aplicación
    path('', inicio_view, name='login'),
]
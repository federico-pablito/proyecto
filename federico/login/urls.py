from django.urls import path
from .views import inicio_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Otras URL de tu aplicación
    path('', inicio_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Internos, Services, UnidadesdeProduccion, Logistica, Novedades, Choferes
from django.contrib.auth.decorators import login_required

# Create your views here.



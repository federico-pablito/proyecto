from django.db import models
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your models here.
class UnidadesProduccionTabla(PermissionRequiredMixin, models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    unidadproduccion = models.CharField(max_length=512)
    ubicacion = models.CharField(max_length=512)
    permission_required = 'unidadproduccion.views_verunidadproduccion'
    permission_required = 'unidadproduccion.views_unidadunidades_pdf_view'

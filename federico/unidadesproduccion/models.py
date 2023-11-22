from django.db import models

# Create your models here.
class UnidadesProduccionTabla(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True)
    unidadproduccion = models.CharField(max_length=512)
    ubicacion = models.CharField(max_length=512)
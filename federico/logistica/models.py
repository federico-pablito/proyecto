from django.db import models
from django.utils import timezone


# solo equipos y produccion
class FormOne(models.Model):
    id = models.AutoField(primary_key=True)
    up_solicita = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_requeridoobra = models.DateTimeField()
    nivel_urgencia = models.ForeignKey('tablamadre.Urgencia', on_delete=models.CASCADE, default=1)
    solicitante = models.CharField(max_length=500)
    repuesto = models.ForeignKey('reparaciones.OrdenDeReparacion', on_delete=models.CASCADE, default=1)
    tipo_equipo = models.CharField(max_length=500)
    descripcion_equipo = models.CharField(max_length=500)
    motivo_requerimiento = models.CharField(max_length=500)
    tope_requerimiento = models.DateTimeField()


# solo produccion
class FormTwo(models.Model):
    id = models.AutoField(primary_key=True)
    up_solicita = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_requeridoobra = models.DateTimeField()
    nivel_urgencia = models.ForeignKey('tablamadre.Urgencia', on_delete=models.CASCADE, default=1)
    solicitante = models.CharField(max_length=500)
    materiales = models.ForeignKey('reparaciones.OrdenDeReparacion', on_delete=models.CASCADE, default=1)
    descripcion = models.CharField(max_length=500)


# produccion y equipos pero con repuestos en vez de maquinas
class FormCombination(models.Model):
    id = models.AutoField(primary_key=True)
    up_solicita = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_requeridoobra = models.DateTimeField()
    nivel_urgencia = models.ForeignKey('tablamadre.Urgencia', on_delete=models.CASCADE, default=1)
    solicitante = models.CharField(max_length=500)
    materiales = models.CharField(max_length=500)
    repuesto = models.ForeignKey('reparaciones.OrdenDeReparacion', on_delete=models.CASCADE, default=1)
    descripcion = models.CharField(max_length=500)
















from datetime import datetime

from django.db import models
from tablamadre.models import Internos


class OrdenDeReparacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    up = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Orden {self.id} - {self.fecha_creacion.strftime('%Y-%m-%d')}"

    class Meta:
        permissions = [
            ("puede_ver_ordenes_reparacion", "Puede ver las ordenes de reparacion"),
            ("puede_crear_ordenes_reparacion", "Puede crear las ordenes de reparacion"),
        ]
        verbose_name_plural = "Ordenes de Reparacion"


class OrdenDeReparacionItem(models.Model):
    orden_de_reparacion = models.ForeignKey('OrdenDeReparacion', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100, default='None')
    nombre = models.CharField(max_length=200, default='None')
    cantidad = models.PositiveIntegerField()
    almacen = models.CharField(max_length=100, default='Central')

    def __str__(self):
        return f"{self.nombre} x {self.cantidad} en Orden {self.orden_de_reparacion.id}"

    class Meta:
        verbose_name_plural = "Items de Orden de Reparacion"


class Reparacion(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('tablamadre.Internos', on_delete=models.CASCADE, default=1)
    taller = models.ForeignKey('Taller', on_delete=models.CASCADE, default=1)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.CASCADE, default=1)
    mecanico_encargado = models.ForeignKey('MecanicoEncargado', on_delete=models.CASCADE, default=1)
    falla_general = models.CharField(max_length=256)
    horas_km_entrada = models.PositiveIntegerField()
    fecha_entrada = models.DateTimeField()
    fecha_reparacion = models.DateTimeField()
    estado_reparacion = models.CharField(max_length=100)
    estado_equipo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=256)
    apto_traslado = models.BooleanField()
    orden_reparacion = models.ForeignKey('OrdenDeReparacion', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Reparacion {self.id} - {self.interno} - {self.fecha_entrada.strftime('%d-%m-%Y')}"

    class Meta:
        permissions = [
            ("puede_ver_reparaciones", "Puede ver las reparaciones"),
            ("puede_crear_reparaciones", "Puede crear las reparaciones"),
        ]
        verbose_name_plural = "Reparaciones"


class Supervisor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Taller(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=512)
    ubicacion = models.CharField(max_length=512)

    def __str__(self):
        return ', '.join([str(self.nombre), str(self.ubicacion)])

    class Meta:
        verbose_name_plural = "Talleres"


class MecanicoEncargado(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=512)
    nombre = models.CharField(max_length=512)
    apellido = models.CharField(max_length=512)
    taller = models.ForeignKey('Taller', on_delete=models.CASCADE, default=1)
    precio_hora = models.PositiveIntegerField()
    archivos_adjuntos = models.FileField(upload_to='Archivos_adjuntos', default='default_value')
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return ', '.join([str(self.codigo), str(self.nombre), str(self.taller)])

    class Meta:
        verbose_name_plural = "Mecanicos Encargados"
        permissions = [
            ("puede_ver_mecanicos_encargados", "Puede ver los mecanicos encargados"),
            ("puede_crear_mecanicos_encargados", "Puede crear los mecanicos encargados"),
        ]


class ParteDiarioMecanicos(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=datetime.now)
    mecanico = models.ForeignKey('MecanicoEncargado', on_delete=models.CASCADE, default=1)
    actividad = models.CharField(max_length=512)
    horas = models.FloatField(default=0.0)

    def __str__(self):
        return f"Parte Diario {self.id} - {self.fecha.strftime('%d-%m-%Y')} - {self.mecanico}"

    class Meta:
        verbose_name_plural = "Partes Diarios Mecanicos"
        permissions = [
            ("puede_ver_partes_diarios_mecanicos", "Puede ver los partes diarios mecanicos"),
            ("puede_crear_partes_diarios_mecanicos", "Puede crear los partes diarios mecanicos"),
        ]

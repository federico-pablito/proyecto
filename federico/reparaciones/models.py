from django.db import models
from tablamadre.models import Internos, Talleres, MecanicosEncargados


class OrdenDeReparacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} - {self.fecha_creacion.strftime('%Y-%m-%d')}"

    class Meta:
        permissions = [
            ("puede_ver_ordenes_reparacion", "Puede ver las ordenes de reparacion"),
            ("puede_crear_ordenes_reparacion", "Puede crear las ordenes de reparacion"),
        ]



class OrdenDeReparacionItem(models.Model):
    orden_de_reparacion = models.ForeignKey('OrdenDeReparacion', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100, default='None')
    nombre = models.CharField(max_length=200, default='None')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.cantidad} en Orden {self.orden_de_reparacion.id}"


class Reparacion(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('tablamadre.Internos', on_delete=models.CASCADE, default=1)
    taller = models.ForeignKey('tablamadre.Talleres', on_delete=models.CASCADE, default=1)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.CASCADE, default=1)
    mecanico_encargado = models.ForeignKey('tablamadre.MecanicosEncargados', on_delete=models.CASCADE, default=1)
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


class Supervisor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

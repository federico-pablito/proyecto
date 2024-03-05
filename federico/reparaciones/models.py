from django.db import models

# Create your models here.


class OrdenDeReparacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} - {self.fecha_creacion.strftime('%Y-%m-%d')}"


class OrdenDeReparacionItem(models.Model):
    orden_de_reparacion = models.ForeignKey('OrdenDeReparacion', on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100, default='None')
    nombre = models.CharField(max_length=200, default='None')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} x {self.cantidad} en Orden {self.orden_de_reparacion.id}"


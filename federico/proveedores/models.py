from django.db import models

# Create your models here.


class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cuit = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.EmailField()
    contacto = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        permissions = [
            ("puede_ver_proveedores", "Puede ver las proveedores"),
            ("puede_crear_proveedores", "Puede crear las proveedores"),
        ]


class EvaluacionProveedor(models.Model):
    id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha = models.DateField()
    calidad = models.PositiveIntegerField()
    cumplimiento_plazo_entrega = models.PositiveIntegerField()
    precio_plazo = models.PositiveIntegerField()

    def __str__(self):
        return f"Evaluacion de {self.proveedor.nombre} - {self.fecha.strftime('%d-%m-%Y')}"

    class Meta:
        verbose_name = 'Evaluacion de Proveedor'
        verbose_name_plural = 'Evaluaciones de Proveedores'
        permissions = [
            ("puede_ver_evaluaciones_proveedores", "Puede ver las evaluaciones de proveedores"),
            ("puede_crear_evaluaciones_proveedores", "Puede crear las evaluaciones de proveedores"),
        ]

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class FormEquipos(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey('SolicitarLogistica', on_delete=models.CASCADE, default=1)
    carreton_propio =  models.BooleanField(default=True)
    proovedor = models.CharField(max_length=500)
    tara = models.DecimalField(max_digits=10, decimal_places=2)
    up_solicita = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    fecha_requeridoobra = models.DateTimeField()
    fecha_envio = models.DateTimeField()
    solicitante = models.CharField(max_length=500)
    equipo = models.ForeignKey('tablamadre.internos', on_delete=models.CASCADE, default=1)
    hsKm = models.IntegerField()
    tope_requerimiento = models.DateTimeField()
    valor_viaje = models.DecimalField(max_digits=10, decimal_places=2)
    chofer = models.ForeignKey('tablamadre.Choferes', on_delete=models.CASCADE, default=1)

    def _str_(self):      
        return f"FormOne ID: {self.id}"



class FormCombination(models.Model):
    id = models.AutoField(primary_key=True)
    id_traslado = models.CharField(max_length=1000)
    carreton_propio = models.BooleanField(default=True)
    equipo_traslada = models.ForeignKey('tablamadre.internos', on_delete=models.CASCADE, default='alquilado')
    proovedor = models.CharField(max_length=500)
    tara = models.DecimalField(max_digits=10, decimal_places=2)
    up_solicita = models.ForeignKey('tablamadre.UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    fecha_requeridoobra = models.DateTimeField()
    fecha_envio = models.DateTimeField()
    descripcion = models.CharField(max_length=500)
    chofer = models.ForeignKey('tablamadre.Choferes', on_delete=models.CASCADE, default=1)
    valor_viaje = models.DecimalField(max_digits=10, decimal_places=2)


    def _str_(self):
        return f"FormCombination ID: {self.id}"



class SolicitarLogistica(models.Model):

    id = models.AutoField(primary_key=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    nivel_urgencia = models.ForeignKey('tablamadre.Urgencia', on_delete=models.CASCADE, default=1)
    tipo_equipo = models.CharField(max_length=500)
    descripcion_equipo = models.CharField(max_length=500)
    motivo_requerimiento = models.CharField(max_length=700)
    fecha_requerido = models.DateTimeField()
    tope_requerimiento = models.DateTimeField()
    observacion = models.CharField(max_length=2000)

    def _str_(self):
        return f"SolicitarLogistica ID: {self.id}"

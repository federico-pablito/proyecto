from django.db import models
from django.utils import timezone

# Create your models here.


class Internos(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.CharField(max_length=50)
	marca = models.CharField(max_length=256)
	modelo = models.CharField(max_length=512)
	chasis = models.CharField(max_length=512)
	motor = models.CharField(max_length=512)
	anio = models.IntegerField()
	aseguradora = models.CharField(max_length=512)
	seguro = models.CharField(max_length=512)
	seguro_pdf = models.CharField(max_length=512, default="No")
	itv = models.CharField(max_length=512)
	itv_pdf = models.CharField(max_length=512, default="No")
	titulo_pdf = models.CharField(max_length=512, default="No")
	tarjeta = models.CharField(max_length=256)
	tarjeta_pdf = models.CharField(max_length=512, default="No")
	# es propietario o proveedor, posibilidad de cambiar eso
	propietario = models.CharField(max_length=512)
	chofer = models.ForeignKey('Choferes', on_delete=models.CASCADE, default=1)
	alquilado = models.BooleanField(default=False)
	valorpesos = models.IntegerField()
	valordolares = models.IntegerField()
	orden = models.CharField(max_length=512)
	actividadvehiculo = models.CharField(max_length=512)
	up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
	dominio = models.CharField(max_length=255, default='default_value')
	tipovehiculo = models.ForeignKey('TipoVehiculo', on_delete=models.CASCADE, default=1)

	class Meta:
		permissions = [
			("puede_ver_internos", "Puede ver los internos"),

		]

	def __str__(self):
		return str(self.interno)


class Services(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	fechaservicio = models.DateTimeField()
	fechaparte = models.DateTimeField()
	ultimoservice = models.IntegerField()
	planrealizado_hs = models.IntegerField()
	planrealizado = models.CharField(max_length=512)
	proximoservice = models.IntegerField()
	hsxkmactuales = models.IntegerField()
	hsxkmrestantes = models.IntegerField()
	necesidadservice = models.CharField(max_length=512)
	operativo = models.CharField(max_length=512, default='Operativo')

	class Meta:
		permissions = [
			("puede_ver_services", "Puede ver los services"),

		]

	def __str__(self):
		return ', '.join([str(self.interno), str(self.fechaservicio), str(self.planrealizado_hs), str(self.planrealizado)])


class UnidadesdeProduccion(models.Model):
	id = models.AutoField(primary_key=True)
	unidadproduccion = models.CharField(max_length=15)
	ubicacion = models.CharField(max_length=512)
	permission_required = 'unidadesproduccion.views_mostrartablamadre'
	permission_denied_message = 'no perro'

	def __str__(self):
		return str(self.unidadproduccion)


class Logistica(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	carreton = models.CharField(max_length=512)
	choferlogistica = models.CharField(max_length=512)
	numeroremito = models.CharField(max_length=512)
	proveedor = models.CharField(max_length=512)
	origen = models.CharField(max_length=512)
	destino = models.CharField(max_length=512)
	kmentredestinos = models.IntegerField()
	transporte = models.CharField(max_length=512)
	consumokmxlitros = models.FloatField(default=0)
	valorviaje = models.IntegerField(default=0)

	class Meta:
		permissions = [
			("puede_ver_logistica", "Puede ver la logistica"),

		]

	def __str__(self):
		return ', '.join([str(self.id), str(self.interno), str(self.numeroremito), str(self.origen), str(self.destino)])


class Novedades(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	reparado = models.BooleanField(default=False)
	tipo_falla = models.CharField(max_length=512, default="Generica")
	fecha = models.DateTimeField(default=timezone.now)
	informacion = models.CharField(max_length=512, default="No hay informacion")
	ingreso_hs_km = models.IntegerField(default=1)
	chofer = models.CharField(max_length=512, default="No tiene chofer")

	class Meta:
		permissions = [
			("puede_ver_novedades", "Puede ver la novedades"),

		]

	def __str__(self):
		return ', '.join([str(self.interno), str(self.reparado), str(self.id)])


class Choferes(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=512)
	anioIngreso = models.DateTimeField()
	dni = models.IntegerField()
	licencia = models.CharField(max_length=512)

	def __str__(self):
		return ' '.join([str(self.nombre), str(self.dni)])


class DisponibilidadEquipos(models.Model):
	id = models.AutoField(primary_key=True)
	up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	chofer = models.ForeignKey('Choferes', on_delete=models.CASCADE, default=1)
	fecha_ingreso_de_obra = models.DateTimeField()
	cantidad_de_dias_en_obra = models.IntegerField()
	anio = models.IntegerField(default=2024)
	mes = models.CharField(max_length=15)
	dia = models.IntegerField()
	actividad = models.ForeignKey('TipoActividad', on_delete=models.CASCADE, default=1)

	class Meta:
		permissions = [
			("puede_ver_disponibilidad", "Puede ver la disponibilidad"),

		]

	def __str__(self):
		return ', '.join([str(self.id), str(self.up), str(self.interno)])


class TipoActividad(models.Model):
	id = models.AutoField(primary_key=True)
	categoria = models.CharField(max_length=1)
	descripcion = models.CharField(max_length=125)

	def __str__(self):
		return ', '.join([self.categoria, self.descripcion])


class Talleres(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=512)
	ubicacion = models.CharField(max_length=512)

	def __str__(self):
		return ', '.join([str(self.nombre), str(self.ubicacion)])


class MecanicosEncargados(models.Model):
	id = models.AutoField(primary_key=True)
	codigo = models.CharField(max_length=512)
	nombre = models.CharField(max_length=512)
	taller = models.ForeignKey('Talleres', on_delete=models.CASCADE, default=1)
	precio_hora = models.PositiveIntegerField()

	def __str__(self):
		return ', '.join([str(self.codigo), str(self.nombre), str(self.taller)])


class AlquilerEquipos(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	solicitante = models.CharField(max_length=512)
	revision = models.CharField(max_length=11, default='REVISIÓN 1')
	r_comp = models.CharField(max_length=10, default='R-COMP-07')
	fecha = models.DateTimeField()
	monto_contratacion = models.IntegerField()
	plazo_pago = models.CharField(max_length=512)
	observaciones_contratacion = models.CharField(max_length=512)
	fecha_inicio_tarea = models.DateTimeField()
	periodo_contratacion = models.CharField(max_length=512)
	periodo_finalizacion = models.CharField(max_length=512)
	up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
	combustible_incluido = models.BooleanField(default=False)
	operario_incluido = models.BooleanField(default=False)
	carnet_operario_vigente = models.BooleanField(default=False)
	carnet_operario_fecha_vencimiento = models.DateTimeField()
	art_operario = models.BooleanField(default=False)
	observaciones_equipo = models.CharField(max_length=512)
	titulo_tarjeta_verde = models.CharField(max_length=512)
	kms = models.IntegerField()
	estado = models.CharField(max_length=7)
	inspeccion_equipo = models.BooleanField(default=False)
	inspeccion_equipo_responsable = models.CharField(max_length=512)
	forma_pago = models.CharField(max_length=512)
	condicion_pago = models.CharField(max_length=512)
	proveedor = models.CharField(max_length=512)
	razon_social = models.CharField(max_length=512)
	cbu = models.CharField(max_length=512)
	telefono = models.CharField(max_length=512)
	autorizado = models.BooleanField(default=False)

	class Meta:
		permissions = [
			("puede_ver_alquilados", "Puede ver los alquilados"),

		]

	def __str__(self):
		return ', '.join([str(self.id), str(self.interno), str(self.solicitante), str(self.fecha)])


class CertificadosEquiposAlquilados(models.Model):
	id = models.AutoField(primary_key=True)
	contratista = models.CharField(max_length=512)
	obra = models.CharField(max_length=512)
	periodo_certificado = models.CharField(max_length=512)
	equipo_alquilado = models.CharField(max_length=512)
	unidad = models.CharField(max_length=3, default='Mes')
	certificado_en_mes = models.FloatField()
	acumulado = models.FloatField()
	precio_unitario = models.FloatField()
	importe = models.FloatField()
	total_neto_deducciones = models.FloatField()
	total_con_iva = models.FloatField()
	fecha = models.DateTimeField(auto_now_add=True)
	mes = models.CharField(max_length=15, default='enero')
	anio = models.IntegerField(default=2024)

	def __str__(self):
		return ', '.join([f'certificado n°{self.id}', str(self.contratista), str(self.equipo_alquilado)])


class HistorialService(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	fechaservicio = models.DateTimeField()
	fechaparte = models.DateTimeField()
	ultimoservice = models.IntegerField()
	planrealizado_hs = models.IntegerField()
	planrealizado = models.CharField(max_length=512)
	proximoservice = models.IntegerField()
	hsxkmactuales = models.IntegerField()
	hsxkmrestantes = models.IntegerField()
	necesidadservice = models.CharField(max_length=512)
	operativo = models.CharField(max_length=512, default='Operativo')

	class Meta:
		permissions = [
			("puede_ver_historial_service", "Puede ver los services"),

		]

	def __str__(self):
		return ', '.join(
			[str(self.interno), str(self.fechaservicio), str(self.planrealizado_hs), str(self.planrealizado)])


class RequerimientoEquipo(models.Model):
	id = models.AutoField(primary_key=True)
	up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
	tipo_equipo = models.CharField(max_length=512)
	fecha_inicial = models.DateTimeField()
	fecha_final = models.DateTimeField()
	solicitante	= models.CharField(max_length=512)
	urgencia = models.CharField(max_length=512)
	aprobado = models.BooleanField(default=False)

	def __str__(self):
		return ', '.join([str(self.id), str(self.tipo_equipo), str(self.up), str(self.aprobado)])


class RequerimientoTraslado(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	origen = models.CharField(max_length=512)
	destino = models.CharField(max_length=512)
	fecha = models.DateTimeField()
	aprobado = models.BooleanField(default=False)

	class Meta:
		permissions = [
			("puede_ver_requerimientos", "Puede ver los requerimientos"),

		]

	def __str__(self):
		return ', '.join([str(self.id), str(self.interno), str(self.origen), str(self.fecha), str(self.aprobado)])


class Cronogroma(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
	fecha = models.DateTimeField()
	motivo_atraso = models.CharField(max_length=512, default='No hay motivo')

	def __str__(self):
		return ', '.join([str(self.id), str(self.interno), str(self.up), str(self.fecha)])


class TipoVehiculo(models.Model):
	id = models.AutoField(primary_key=True)
	tipo = models.CharField(max_length=512)

	def __str__(self):
		return str(self.tipo)


class Urgencia(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=512)

	def __str__(self):
		return str(self.nombre)


class FiltrosInternos(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	filtro = models.CharField(max_length=512)
	marca = models.CharField(max_length=512)
	codigo = models.CharField(max_length=512)

	def __str__(self):
		return ', '.join([str(self.interno), str(self.filtro), str(self.marca), str(self.codigo)])


class NeumaticosInternos(models.Model):
	id = models.AutoField(primary_key=True)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	marca = models.CharField(max_length=512)
	medida = models.CharField(max_length=512)
	codigo = models.CharField(max_length=512)

	def __str__(self):
		return ', '.join([str(self.interno), str(self.marca), str(self.codigo)])


class Tanque(models.Model):
	nombre = models.CharField(primary_key=True, max_length=255)
	capacidad = models.DecimalField(max_digits=10, decimal_places=2)
	cantidad_combustible = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		permissions = [
			("puede_ver_tanques", "Puede ver los tanques"),

		]

	def __str__(self):
		return ', '.join([str(self.nombre), str(self.capacidad), str(self.cantidad_combustible)])


class Consumo(models.Model):
	id = models.AutoField(primary_key=True)
	tanque = models.ForeignKey('Tanque', on_delete=models.CASCADE, default=1)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	chofer = models.ForeignKey('Choferes', on_delete=models.CASCADE, default=1)
	consumo_litros = models.DecimalField(max_digits=10, decimal_places=2)
	fecha_consumo = models.DateTimeField()
	hskmactuales = models.IntegerField()
	precinto_entrada = models.IntegerField()
	precinto_salida = models.IntegerField()
	observaciones = models.CharField(max_length=600)

	class Meta:
		permissions = [
			("puede_ver_consumo", "Puede ver los consumos"),

		]

	def __str__(self):
		return ', '.join([str(self.tanque), str(self.interno), str(self.chofer), str(self.consumo_litros), str(self.fecha_consumo)])


class Repostaje(models.Model):
	id = models.AutoField(primary_key=True)
	tanque = models.ForeignKey('Tanque', on_delete=models.CASCADE, default=1)
	cantidad_litros = models.DecimalField(max_digits=10, decimal_places=2)
	fecha = models.DateTimeField(default=timezone.now)
	remito = models.IntegerField(default=00000)
	proveedor = models.CharField(max_length=512, default="PabloFederico")

	class Meta:
		permissions = [
			("puede_ver_repostaje", "Puede ver los repostajes"),

		]

	def __str__(self):
		return ', '.join([str(self.tanque), str(self.cantidad_litros), str(self.fecha), str(self.remito), str(self.proveedor)])


class TanqueAceite(models.Model):
	nombre = models.CharField(primary_key=True, max_length=100)
	tipo_aceite = models.CharField(max_length=100)
	capacidad_aceite = models.DecimalField(max_digits=10, decimal_places=2)
	cantidad_aceite = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		permissions = [
			("puede_ver_aceites", "Puede ver los aceites"),

		]


class ConsumoAceite(models.Model):
	id = models.AutoField(primary_key=True)
	tanque_aceite = models.ForeignKey('TanqueAceite', on_delete=models.CASCADE, default=1)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	chofer = models.ForeignKey('Choferes', on_delete=models.CASCADE, default=1)
	cantidad_consumida = models.DecimalField(max_digits=10, decimal_places=2)
	fecha_consumo = models.DateTimeField()
	hskmactuales = models.IntegerField()
	observaciones = models.CharField(max_length=500)

	class Meta:
		permissions = [
			("puede_ver_consumoaceite", "Puede ver los consumos de aceite"),

		]


class RepostajeAceite(models.Model):
	remito = models.IntegerField(primary_key=True)
	reservorio_aceite = models.ForeignKey('TanqueAceite', on_delete=models.CASCADE, default=1)
	fecha_repostaje = models.DateTimeField()
	cantidad_repostada = models.DecimalField(max_digits=10, decimal_places=2)
	observaciones = models.CharField(max_length=500)

	class Meta:
		permissions = [
			("puede_ver_cargarrepostaje", "Puede ver los repostajes de aceites"),

		]

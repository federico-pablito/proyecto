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
	seguro_pdf = models.FileField(upload_to='Seguros', default='default_value')
	itv = models.FileField(upload_to='ITV', default='default_value')
	titulo = models.FileField(upload_to='Titulos', default='default_value')
	tarjeta = models.FileField(upload_to='Tarjetas', default='default_value')
	# es propietario o proveedor, posibilidad de cambiar eso
	propietario = models.CharField(max_length=512)
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
			("puede_ver_info_internos", "Puede ver los info internos"),

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
	apellido = models.CharField(max_length=512)
	fecha_ingreso = models.DateField()
	dni = models.BigIntegerField()
	licencia = models.FileField(upload_to='Licencias', default='default_value')
	dni_pdf = models.FileField(upload_to='DNI', default='default_value')
	usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)

	def __str__(self):
		return ' '.join([str(self.nombre), str(self.apellido), str(self.dni)])

	class Meta:
		permissions = [
			("puede_ver_choferes", "Puede ver los choferes"),
			("puede_crear_choferes", "Puede crear los choferes")
		]


class Operadores(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=512)
	apellido = models.CharField(max_length=512)
	fecha_ingreso = models.DateField()
	dni = models.BigIntegerField()
	licencia = models.FileField(upload_to='Licencias', default='default_value')
	dni_pdf = models.FileField(upload_to='DNI', default='default_value')
	usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)

	def __str__(self):
		return ' '.join([str(self.nombre), str(self.apellido), str(self.dni)])

	class Meta:
		permissions = [
			("puede_ver_operadores", "Puede ver los operadores"),
			("puede_crear_operadores", "Puede crear los operadores")
		]


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
	art_operario = models.FileField(upload_to='ART', default='default_value')
	observaciones_equipo = models.CharField(max_length=512)
	titulo_tarjeta_verde = models.FileField(upload_to='Titulos', default='default_value')
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
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
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
		return ', '.join([f'certificado n°{self.id}', str(self.contratista), str(self.equipo_alquilado), str(self.interno.interno)])


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
	hskmactuales = models.BigIntegerField()
	precinto_entrada = models.BigIntegerField()
	precinto_salida = models.BigIntegerField()
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
	remito = models.CharField(unique=True, max_length=100)
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

	def __str__(self):
		return self.nombre.title()

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
	remito = models.CharField(primary_key=True, unique=True, max_length=100)
	reservorio_aceite = models.ForeignKey('TanqueAceite', on_delete=models.CASCADE, default=1)
	fecha_repostaje = models.DateTimeField()
	cantidad_repostada = models.DecimalField(max_digits=10, decimal_places=2)
	observaciones = models.CharField(max_length=500)

	class Meta:
		permissions = [
			("puede_ver_cargarrepostaje", "Puede ver los repostajes de aceites"),

		]


class FotoVehiculos(models.Model):
	id = models.AutoField(primary_key=True)
	fecha = models.DateTimeField(default=timezone.now)
	titulo = models.CharField(max_length=512, default='Foto')
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	foto = models.ImageField(upload_to='FotosVehiculos', default='default_value')

	def __str__(self):
		return f'Foto de {self.interno}'


class ArchivosAdjuntos(models.Model):
	id = models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=512)
	interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
	archivo = models.FileField(upload_to='ArchivosAdjuntos', default='default_value')

	def __str__(self):
		return f'Archivo de {self.interno} {self.titulo}'

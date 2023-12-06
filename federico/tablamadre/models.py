from django.db import models

# Create your models here.
class TablaMadre(models.Model):
    id = models.AutoField(primary_key=True, serialize=True, auto_created=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    internos = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
    services = models.ForeignKey('Services', on_delete=models.CASCADE, default=1)
    unidadesdeproduccion = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    reparaciones = models.ForeignKey('Reparaciones', on_delete=models.CASCADE, default=1)
    logistica = models.ForeignKey('Logistica', on_delete=models.CASCADE, default=1)
    dolardia = models.IntegerField()
    partesdiarions = models.ForeignKey('PartesDiarios', on_delete=models.CASCADE, default=1)
    observaciones = models.CharField(max_length=512)
    def __str__(self):
        return ', '.join([str(self.internos), str(self.services), str(self.unidadesdeproduccion), str(self.reparaciones), str(self.logistica), str(self.dolardia), str(self.partesdiarions), str(self.novedades), str(self.observaciones), str(self.id)])


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
    seguro_pdf = models.CharField(max_length=512)
    itv = models.CharField(max_length=512)
    itv_pdf = models.CharField(max_length=512)
    titulo_pdf = models.CharField(max_length=512)
    tarjeta = models.CharField(max_length=256)
    tarjeta_pdf = models.CharField(max_length=512)
    # es propietario o proveedor, posibilidad de cambiar eso
    propietario = models.CharField(max_length=512)
    chofer = models.CharField(max_length=512)
    alquilado = models.BooleanField(default=False)
    valorpesos = models.IntegerField()
    valordolares = models.IntegerField()
    orden = models.CharField(max_length=512)
    actividadvehiculo = models.CharField(max_length=512)
    up = models.ForeignKey('UnidadesdeProduccion', on_delete=models.CASCADE, default=1)
    dominio = models.CharField(max_length=255, default='default_value')
    tipovehiculo = models.CharField(max_length=255, default='valor_predeterminado')

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
    def __str__(self):
        return ', '.join([str(self.interno), str(self.fechaservicio), str(self.fechaparte), str(self.ultimoservice), str(self.planrealizado_hs), str(self.planrealizado), str(self.proximoservice), str(self.hsxkmactuales), str(self.hsxkmrestantes), str(self.necesidadservice), str(self.id)])


class UnidadesdeProduccion(models.Model):
    id = models.AutoField(primary_key=True)
    unidadproduccion = models.CharField(max_length=15)
    ubicacion = models.CharField(max_length=512)
    def __str__(self):
        return str(self.unidadproduccion)

class Reparaciones(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
    ubicacion = models.CharField(max_length=512, default='Taller')
    falla = models.CharField(max_length=512)
    porcentajeavance = models.IntegerField()
    fechareparacionestimada = models.DateTimeField()
    fechaentrada = models.DateTimeField()
    fechasalida = models.DateTimeField()
    estadoreparacion = models.CharField(max_length=512)
    estadoequipo = models.CharField(max_length=512)
    def __str__(self):
        return ', '.join([str(self.id), str(self.interno), str(self.ubicacion), str(self.falla), str(self.porcentajeavance),
                          str(self.fechareparacionestimada), str(self.fechaentrada), str(self.fechasalida),
                          str(self.estadoreparacion), str(self.estadoequipo)])


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
    consumokmxlitros = models.IntegerField()
    valorviaje = models.IntegerField()

    def __str__(self):
        return ', '.join([str(self.interno), str(self.carreton), str(self.choferlogistica), str(self.numeroremito),
                          str(self.proveedor), str(self.origen), str(self.destino), str(self.kmentredestinos),
                          str(self.transporte), str(self.consumokmxlitros), str(self.valorviaje), str(self.id)])


class PartesDiarios(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
    proveedores = models.CharField(max_length=512)
    razon_social = models.CharField(max_length=512)
    cantida_de_quipos = models.IntegerField()
    kilometraje_inicial = models.IntegerField()
    kilometraje_final = models.IntegerField()
    turno_reparacion = models.CharField(max_length=512)
    horometro = models.IntegerField()
    hsxkmcarga = models.IntegerField()
    tipo_combustible = models.CharField(max_length=512)
    tipo_gasoil = models.CharField(max_length=512)
    tipo_nafta = models.CharField(max_length=512)
    litros_gasoil = models.IntegerField()
    litros_nafta = models.IntegerField()
    tipo_aceite = models.CharField(max_length=512)
    litros_aceite = models.IntegerField()
    maquinista = models.CharField(max_length=512)
    kmsxhs = models.IntegerField()
    tipo_de_falla = models.CharField(max_length=512, default='No hay falla')
    reparado = models.BooleanField(default=False)
    def __str__(self):
        return ', '.join([str(self.interno), str(self.proveedores), str(self.razonsocial), str(self.cantidadequipos), str(self.kilometrajeinicial), str(self.kilometrajefinal), str(self.turnoreparacion), str(self.horometro), str(self.hsxkmcarga), str(self.tipocombustible), str(self.tipogasoil), str(self.tiponafta), str(self.litrosgasoil), str(self.litrosnafta), str(self.tipoaceite), str(self.litrosaceite), str(self.maquinista), str(self.kmsxhs), str(self.id), str(self.tipodefalla), str(self.reparado)])
class Novedades(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1)
    reparado = models.BooleanField(default=False)
def __str__(self):
        return ', '.join([str(self.interno), str(self.tipofalla), str(self.reparado), str(self.id)])

class Choferes(models.Model):
     id = models.AutoField(primary_key=True)
     nombre = models.CharField(max_length=512)
     añoIngreso = models.DateTimeField()
     dni = models.IntegerField()
     licencia = models.CharField(max_length=512)
def __str__(self):
    return ', '.join([str(self.id), str(self.nombre), str(self.añoingreso), str(self.dni),str(self.licencia)])
      
    
class Consumos(models.Model):
    id = models.AutoField(primary_key=True)
    interno = models.ForeignKey('Internos', on_delete=models.CASCADE, default=1) 
    fecha = models.DateTimeField()
    hsKm = models.IntegerField()
    choferes = models.ForeignKey('Choferes', on_delete=models.CASCADE, default=1)
def __str__(self):
     return ', '.join([str(self.id), str(self.interno), str(self.fecha), str(self.hsKM),str(self.choferes)])
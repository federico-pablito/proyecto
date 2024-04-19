from django import forms
from tablamadre.models import Internos, UnidadesdeProduccion, AlquilerEquipos, CertificadosEquiposAlquilados, \
    FiltrosInternos, TipoVehiculo, Choferes, Operadores, FotoVehiculos, ArchivosAdjuntos
from django.contrib.auth.models import User


class internosforms(forms.ModelForm):
    interno = forms.CharField(required=True)
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=True,
                                label='UP')
    marca = forms.CharField(required=True)
    modelo = forms.CharField(required=True)
    tipovehiculo = forms.ModelChoiceField(queryset=TipoVehiculo.objects.all(), empty_label=None, required=True)
    chasis = forms.CharField(required=True)
    motor = forms.CharField(required=True)
    dominio = forms.CharField(required=True)
    anio = forms.IntegerField(required=True, label='Año')
    aseguradora = forms.CharField(required=True, label='Aseguradora')
    seguro = forms.CharField(required=True)
    seguro_pdf = forms.FileField()
    itv = forms.FileField()
    titulo = forms.FileField()
    tarjeta = forms.FileField()
    propietario = forms.CharField(required=True)
    alquilado = forms.ChoiceField(choices=[(False, 'No'), (True, 'Si')], required=False, label='Alquilado')
    valorpesos = forms.IntegerField(required=True, label='Valor Ars')
    valordolares = forms.IntegerField(required=True, label='Valor Usd')
    orden = forms.CharField(required=True)
    actividadvehiculo = forms.CharField(required=True, label='Act Vehiculo')
    descripcion = forms.CharField(required=False)

    class Meta:
        model = Internos
        fields = ['interno', 'up', 'marca', 'modelo', 'tipovehiculo', 'chasis', 'motor', 'dominio', 'anio',
                    'aseguradora', 'seguro', 'seguro_pdf', 'itv', 'titulo', 'tarjeta', 'propietario', 'alquilado',
                    'valorpesos', 'valordolares', 'orden', 'actividadvehiculo', 'descripcion']


class AlquilerEquiposForm(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label='Seleccione un interno', required=True)
    solicitante = forms.CharField(required=True)
    fecha = forms.DateField(required=True,
                            widget=forms.DateInput(attrs={'type': 'date'}),
                            label='Fecha')
    monto_contratacion = forms.IntegerField(required=True)
    plazo_pago = forms.CharField(required=True)
    observaciones_contratacion = forms.CharField(required=False)
    fecha_inicio_tarea = forms.DateField(required=True,
                                         widget=forms.DateInput(attrs={'type': 'date'}),
                                         label='Inicio Act')
    periodo_contratacion = forms.CharField(required=True)
    periodo_finalizacion = forms.CharField(required=True)
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False,
                                label='Unidad de Prod')
    combustible_incluido = forms.BooleanField(required=False, initial=False)
    operario_incuido = forms.BooleanField(required=False, initial=False)
    carnet_operario_vigente = forms.BooleanField(required=False, initial=False)
    carnet_operario_fecha_vencimiento = forms.DateField(required=True,
                                                        widget=forms.DateInput(attrs={'type': 'date'}),
                                                        label='Fecha')
    art_operario = forms.BooleanField(required=False, initial=False)
    observaciones_equipo = forms.CharField(required=False)
    titulo_tarjeta_verde = forms.CharField(required=True)
    kms = forms.IntegerField(required=True)
    estado = forms.CharField(required=True)
    seguro_equipo = forms.BooleanField(required=True)
    inspeccion_equipo = forms.BooleanField(required=True)
    inspeccion_equipo_responsable = forms.CharField(required=True)
    forma_pago = forms.CharField(required=True)
    condicion_pago = forms.CharField(required=True)
    proveedor = forms.CharField(required=True)
    razon_social = forms.CharField(required=True)
    cbu = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    autorizado = forms.BooleanField(required=True)

    class Meta:
        model = AlquilerEquipos
        fields = ['interno', 'solicitante', 'fecha', 'monto_contratacion', 'plazo_pago', 'observaciones_contratacion',
                  'fecha_inicio_tarea', 'periodo_contratacion', 'periodo_finalizacion', 'up', 'combustible_incluido',
                  'operario_incuido', 'carnet_operario_vigente', 'carnet_operario_fecha_vencimiento', 'art_operario',
                  'observaciones_equipo', 'titulo_tarjeta_verde', 'kms',
                  'estado', 'seguro_equipo', 'inspeccion_equipo', 'inspeccion_equipo_responsable', 'forma_pago',
                  'condicion_pago', 'proveedor', 'razon_social', 'cbu', 'telefono', 'autorizado']



class CertificadosEquiposAlquiladosForm(forms.Form):
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
             'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    anios = ['2023', '2024', '2025', '2026', '2027']
    OPCIONES = []
    for anio in anios:
        for mes in meses:
            OPCIONES.append((mes + ' ' + anio, mes + ' ' + anio))
    fecha = forms.ChoiceField(choices=OPCIONES, widget=forms.Select, label='Fecha')


class FiltroForm(forms.Form):
    filtro = forms.CharField(required=True, label='Filtro')
    marca = forms.CharField(required=True, label='Marca')
    codigo = forms.CharField(required=True, label='Codigo')

    class Meta:
        model = FiltrosInternos
        fields = ['filtro', 'marca', 'codigo']


class NeumaticoForm(forms.Form):
    marca = forms.CharField(required=True, label='Marca')
    medida = forms.CharField(required=True, label='Filtro')
    codigo = forms.CharField(required=True, label='Codigo')

    class Meta:
        model = FiltrosInternos
        fields = ['marca', 'medida', 'codigo']


class ChoferesForm(forms.ModelForm):
    fecha_ingreso = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha Ingreso')
    dni = forms.IntegerField()
    licencia = forms.FileField()
    dni_pdf = forms.FileField()
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, required=True)

    class Meta:
        model = Choferes
        fields = ['fecha_ingreso', 'dni', 'licencia', 'dni_pdf', 'usuario']


class OperariosForm(forms.ModelForm):
    fecha_ingreso = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha Ingreso')
    dni = forms.IntegerField()
    licencia = forms.FileField()
    dni_pdf = forms.FileField()
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, required=True)

    class Meta:
        model = Operadores
        fields = ['fecha_ingreso', 'dni', 'licencia', 'dni_pdf', 'usuario']


class fotosform(forms.ModelForm):
    titulo = forms.CharField(required=True)
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=True)
    foto = forms.FileField()
    class Meta:
        model = FotoVehiculos
        fields = ['titulo', 'interno', 'foto']


class adjuntosform(forms.ModelForm):
    titulo = forms.CharField(required=True)
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=True)
    archivo = forms.FileField()
    class Meta:
        model = ArchivosAdjuntos
        fields = ['titulo', 'interno', 'archivo']


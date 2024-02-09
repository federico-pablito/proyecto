from django import forms
from tablamadre.models import Internos, UnidadesdeProduccion, AlquilerEquipos, CertificadosEquiposAlquilados, FiltrosInternos


class internosforms(forms.ModelForm):
    interno = forms.CharField(required=True)
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=True,
                                label='UP')
    marca = forms.CharField(required=True)
    modelo = forms.CharField(required=True)
    tipovehiculo = forms.CharField(required=True, label='Tipo V')
    chasis = forms.CharField(required=True)
    motor = forms.CharField(required=True)
    dominio = forms.CharField(required=True)
    anio = forms.IntegerField(required=True, label='Año')
    aseguradora = forms.CharField(required=True, label='Aseguradora')
    seguro = forms.CharField(required=True)
    seguro_pdf = forms.CharField(required=False)
    itv = forms.CharField(required=False)
    itv_pdf = forms.CharField(required=False)
    titulo_pdf = forms.CharField(required=False)
    tarjeta = forms.CharField(required=False)
    tarjeta_pdf = forms.CharField(required=False)
    propietario = forms.CharField(required=True)
    chofer = forms.CharField(required=True)
    alquilado = forms.BooleanField(required=False, initial=False)
    valorpesos = forms.IntegerField(required=True, label='Valor Ars')
    valordolares = forms.IntegerField(required=True, label='Valor Usd')
    orden = forms.CharField(required=True)
    actividadvehiculo = forms.CharField(required=True, label='Act Vehiculo')
    descripcion = forms.CharField(required=False)

    class Meta:
        model = Internos
        fields = ['interno', 'marca', 'modelo', 'tipovehiculo', 'chasis', 'motor', 'dominio', 'anio', 'aseguradora',
                  'seguro', 'seguro_pdf', 'itv',
                  'tarjeta', 'propietario', 'chofer', 'alquilado', 'valorpesos',
                  'valordolares', 'orden', 'actividadvehiculo', 'up']
        widgets = {
            'interno': forms.TextInput(attrs={'class': 'mi_clase', 'placeholder': 'Mi placeholder'}),
            # add your other fields with their widgets here
        }


class TableVariable(forms.Form):
    id_value = forms.BooleanField(required=False, label='ID', initial=True)
    interno_value = forms.BooleanField(required=False, label='Interno', initial=True)
    up_value = forms.BooleanField(required=False, label='UP', initial=True)
    marca_value = forms.BooleanField(required=False, label='Marca', initial=True)
    modelo_value = forms.BooleanField(required=False, label='Modelo', initial=True)
    tipovehiculo_value = forms.BooleanField(required=False, label='T.Vehiculo', initial=True)
    chasis_value = forms.BooleanField(required=False, label='Chasis', initial=False)
    motor_value = forms.BooleanField(required=False, label='Motor', initial=False)
    dominio_value = forms.BooleanField(required=False, label='Dominio', initial=True)
    anio_value = forms.BooleanField(required=False, label='Año', initial=True)
    aseguradora_value = forms.BooleanField(required=False, label='Aseguradora', initial=False)
    seguro_value = forms.BooleanField(required=False, label='Seguro', initial=False)
    seguro_pdf_value = forms.BooleanField(required=False, label='Seg PDF', initial=False)
    itv_value = forms.BooleanField(required=False, label='ITV', initial=False)
    itv_pdf_value = forms.BooleanField(required=False, label='ITV PDF', initial=False)
    titulo_pdf_value = forms.BooleanField(required=False, label='Archivos', initial=False)
    tarjeta_value = forms.BooleanField(required=False, label='Tarjeta', initial=False)
    tarjeta_pdf_value = forms.BooleanField(required=False, label='T PDF', initial=False)
    propietario_value = forms.BooleanField(required=False, label='Dueño', initial=True)
    chofer_value = forms.BooleanField(required=False, label='Chofer', initial=True)
    alquilado_value = forms.BooleanField(required=False, label='Alquilado', initial=False)
    valorpesos_value = forms.BooleanField(required=False, label='Valor P', initial=False)
    valordolares_value = forms.BooleanField(required=False, label='Valor D', initial=False)
    orden_value = forms.BooleanField(required=False, label='Orden', initial=True)
    actividad_value = forms.BooleanField(required=False, label='Actividad', initial=True)

    class Meta:
        fields = ['id_value', 'interno_value', 'marca_value', 'modelo_value', 'tipovehiculo_value', 'chasis_value', 'motor_value',
                  'dominio_value', 'anio_value', 'aseguradora_value', 'seguro_value', 'seguro_pdf_value', 'itv_value',
                  'itv_pdf_value', 'titulo_pdf_value', 'tarjeta_value', 'tarjeta_pdf_value', 'propietario_value',
                  'chofer_value', 'alquilado_value', 'valorpesos_value', 'valordolares_value', 'orden_value',
                  'up_value', 'actividad_value', 'orden_value']


class AlquilerEquiposForm(forms.ModelForm):
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
    tipo_vehiculo = forms.CharField(required=True)
    modelo = forms.CharField(required=True)
    marca = forms.CharField(required=True)
    dominio = forms.CharField(required=True)
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
        fields = ['solicitante', 'fecha', 'monto_contratacion', 'plazo_pago', 'observaciones_contratacion',
                  'fecha_inicio_tarea', 'periodo_contratacion', 'periodo_finalizacion', 'up', 'combustible_incluido',
                  'operario_incuido', 'carnet_operario_vigente', 'carnet_operario_fecha_vencimiento', 'art_operario',
                  'observaciones_equipo', 'tipo_vehiculo', 'modelo', 'marca', 'dominio', 'titulo_tarjeta_verde', 'kms',
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

from django import forms
from tablamadre.models import (Logistica, Internos, UnidadesdeProduccion, TipoVehiculo, Urgencia, RequerimientoEquipo,
                               RequerimientoTraslado, Cronogroma)


class logistica_form(forms.ModelForm):
    model = Logistica
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    carreton = forms.CharField(required=True)
    choferlogistica = forms.CharField(required=True)
    numeroremito = forms.CharField(required=True)
    proveedor = forms.CharField(required=True)
    origen = forms.CharField(required=True)
    destino = forms.CharField(required=True)
    kmentredestinos = forms.IntegerField(required=True)
    transporte = forms.CharField(required=True)
    consumokmxlitros = forms.IntegerField(required=True)
    valorviaje = forms.IntegerField(required=True)
    descripcion = forms.CharField(required=False)
    class Meta:
        model = Logistica
        fields = ['interno', 'carreton', 'choferlogistica', 'numeroremito', 'proveedor', 'origen', 'destino',
                  'kmentredestinos', 'transporte', 'consumokmxlitros', 'valorviaje']


class requerimiento_equipo_form(forms.ModelForm):
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False, label='UP')
    tipo_equipo = forms.ModelChoiceField(queryset=TipoVehiculo.objects.all(), empty_label=None, required=False, label='Tipo de Equipo')
    fecha_inicial = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fecha_final = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    solicitante = forms.CharField(required=True)
    urgencia = forms.ModelChoiceField(queryset=Urgencia.objects.all(), empty_label=None, required=False, label='Urgencia')

    class Meta:
        model = RequerimientoEquipo
        fields = ['up', 'tipo_equipo', 'fecha_inicial', 'fecha_final', 'solicitante', 'urgencia']
        widgets = {
            'fecha_inicial': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }


class requerimiento_traslado_form(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    origen = forms.CharField(required=True)
    destino = forms.CharField(required=True)
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )

    class Meta:
        model = RequerimientoTraslado
        fields = ['interno', 'origen', 'destino', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


class cronograma_form(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False, label='UP')
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    motivo_retraso = forms.CharField(required=True)

    class Meta:
        model = Cronogroma
        fields = ['interno', 'up', 'fecha', 'motivo_retraso']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

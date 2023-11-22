from django import forms
from tablamadre.models import Internos, UnidadesdeProduccion

class internosforms(forms.ModelForm):
    interno = forms.CharField(required=True)
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False, label='Unidad de Produccion')
    marca = forms.CharField(required=True)
    modelo = forms.CharField(required=True)
    tipovehiculo = forms.CharField(required=True)
    chasis = forms.CharField(required=True)
    motor = forms.CharField(required=True)
    dominio = forms.CharField(required=True)
    anio = forms.IntegerField(required=True)
    aseguradora = forms.CharField(required=True)
    seguro = forms.CharField(required=True)
    seguro_pdf = forms.CharField(required=True)
    itv = forms.CharField(required=False)
    itv_pdf = forms.CharField(required=False)
    titulo_pdf = forms.CharField(required=True)
    tarjeta = forms.CharField(required=False)
    tarjeta_pdf = forms.CharField(required=False)
    propietario = forms.CharField(required=True)
    chofer = forms.CharField(required=True)
    alquilado = forms.BooleanField(required=False, initial=False)
    valorpesos = forms.IntegerField(required=True)
    valordolares = forms.IntegerField(required=True)
    orden = forms.CharField(required=True)
    actividadvehiculo = forms.CharField(required=True)
    descripcion = forms.CharField(required=False)
    class Meta:
        model = Internos
        fields = ['interno', 'marca', 'modelo', 'tipovehiculo','chasis', 'motor','dominio', 'anio', 'aseguradora', 'seguro', 'seguro_pdf', 'itv',
                  'itv_pdf', 'titulo_pdf', 'tarjeta', 'tarjeta_pdf', 'propietario', 'chofer', 'alquilado', 'valorpesos',
                  'valordolares', 'orden', 'actividadvehiculo', 'up']

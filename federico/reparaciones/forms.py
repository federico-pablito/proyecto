from django import forms
from .models import Reparacion, Supervisor, OrdenDeReparacion, Taller, MecanicoEncargado, ParteDiarioMecanicos
from tablamadre.models import Internos, UnidadesdeProduccion


class ReparacionForm(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=True, label='Interno')
    taller = forms.ModelChoiceField(queryset=Taller.objects.all(), empty_label=None, required=True, label='Taller')
    supervisor = forms.ModelChoiceField(queryset=Supervisor.objects.all(), empty_label=None, required=True, label='Supervisor')
    mecanico_encargado = forms.ModelChoiceField(queryset=MecanicoEncargado.objects.all(), empty_label=None, required=True, label='Mecanico Encargado')
    falla_general = forms.CharField(required=True, label='Falla General')
    horas_km_entrada = forms.IntegerField(required=True, label='Horas/Km de Entrada')
    fecha_entrada = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Entrada')
    fecha_reparacion = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Reparacion')
    estado_reparacion = forms.ChoiceField(choices=[('Pendiente', 'Pendiente'), ('Completo', 'Completo')], required=True, label='Estado de Reparacion')
    estado_equipo = forms.ChoiceField(choices=[('Operativo', 'Operativo'), ('No Operativo', 'No Operativo')], required=True, label='Estado de Equipo')
    descripcion = forms.CharField(required=True, label='Descripcion')
    apto_traslado = forms.BooleanField(required=False, label='Apto para Traslado')
    orden_reparacion = forms.ModelChoiceField(queryset=OrdenDeReparacion.objects.all(), empty_label=None, required=True, label='Orden de Reparacion')

    class Meta:
        model = Reparacion
        fields = '__all__'
        exclude = ['id']


class OrdenForm(forms.ModelForm):
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=True)

    class Meta:
        fields = ['up']
        model = OrdenDeReparacion
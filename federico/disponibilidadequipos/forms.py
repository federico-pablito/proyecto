from django import forms
from tablamadre.models import Internos, UnidadesdeProduccion, TipoActividad

class disponibilidad_form(forms.ModelForm):
    MESES_OPCIONES=(('enero', 'Enero'),
                    ('febrero', 'Febrero'),
                    ('marzo', 'Marzo'),
                    ('abril', 'Abril'),
                    ('mayo', 'Mayo'),
                    ('junio', 'Junio'),
                    ('julio', 'Julio'),
                    ('agosto', 'Agosto'),
                    ('septiembre', 'Septiembre'),
                    ('octubre', 'Octubre'),
                    ('noviembre', 'Noviembre'),
                    ('diciembre', 'Diciembre'))
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False, label='Unidad de Produccion')
    fecha_ingreso_de_obra = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de Ingreso de Obra'
    )
    anio = forms.IntegerField(required=True, label='Año')
    mes = forms.ChoiceField(choices=MESES_OPCIONES, widget=forms.Select, label='Mes')
    dia = forms.IntegerField(required=True, label='Dia')
    actividad = forms.ModelChoiceField(queryset=TipoActividad.objects.all(), empty_label=None, required=False, label='Actividad')

    class Meta:
        model = Internos
        fields = ['interno', 'marca', 'modelo', 'tipovehiculo','chasis', 'motor','dominio', 'anio', 'aseguradora', 'seguro', 'seguro_pdf', 'itv',
                  'itv_pdf', 'titulo_pdf', 'tarjeta', 'tarjeta_pdf', 'propietario', 'chofer', 'alquilado', 'valorpesos',
                  'valordolares', 'orden', 'actividadvehiculo', 'up']

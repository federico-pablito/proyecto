from django import forms
from tablamadre.models import Internos, UnidadesdeProduccion, TipoActividad, Choferes, DisponibilidadEquipos

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
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=True, label='Internos')
    chofer = forms.ModelChoiceField(queryset=Choferes.objects.all(), empty_label=None, required=True, label='Choferes')
    up = forms.ModelChoiceField(queryset=UnidadesdeProduccion.objects.all(), empty_label=None, required=False, label='UP')
    fecha_ingreso_de_obra = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de Ingreso'
    )
    anio = forms.IntegerField(required=True, label='Año')
    mes = forms.ChoiceField(choices=MESES_OPCIONES, widget=forms.Select, label='Mes')
    dia = forms.IntegerField(required=True, label='Dia')
    actividad = forms.ModelChoiceField(queryset=TipoActividad.objects.all(), empty_label=None, required=False, label='Actividad')
    cantidad_de_dias_en_obra = forms.IntegerField(required=True, label='Dias en Obra')

    class Meta:
        model = DisponibilidadEquipos
        fields = ['interno', 'chofer', 'up', 'fecha_ingreso_de_obra', 'anio', 'mes', 'dia', 'actividad', 'cantidad_de_dias_en_obra']

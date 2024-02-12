from django import forms
from tablamadre.models import Reparaciones, Services, Internos, MecanicosEncargados, Talleres


class reparaciones_form(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Unidad de Produccion')
    taller = forms.ModelChoiceField(queryset=Talleres.objects.all(), empty_label=None, required=False, label='Taller')
    mecanico_encargado = forms.ModelChoiceField(queryset=MecanicosEncargados.objects.all(), empty_label=None, required=False, label='Mecanico Encargado')
    falla_general = forms.CharField(max_length=50)
    fechareparacionestimada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fechaentrada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fechasalida = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    estadoreparacion = forms.ChoiceField(choices=(('Pendiente', 'Pendiente'), ('Completo', 'Completo')),
                                         widget=forms.Select, label='Estado de Reparacion')
    estadoequipo = forms.ChoiceField(choices=(('No Operativo', 'No Operativo'), ('Operativo', 'Operativo')))
    apto_traslado = forms.BooleanField(required=False)
    descripcion = forms.CharField(required=True)

    class Meta:
        model = Reparaciones
        fields = ['interno', 'taller', 'mecanico_encargado', 'falla_general', 'fechareparacionestimada', 'fechaentrada',
                  'fechasalida', 'estadoreparacion', 'descripcion', 'estadoequipo', 'apto_traslado']

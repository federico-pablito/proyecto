from django import forms
from tablamadre.models import Internos, Novedades


class novedadesforms(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=True, label='Interno')
    tipo_falla = forms.CharField(required=True, label='Tipo de Falla')
    fecha = forms.DateField(required=True,
                            widget=forms.DateInput(attrs={'type': 'date'}),
                            label='Fecha')
    informacion = forms.CharField(required=True, label='Información')
    ingreso_hs_km = forms.IntegerField(required=True, label='Ingreso Hs/Km')
    chofer = forms.CharField(required=True, label='Chofer')

    class Meta:
        model = Novedades
        fields = ['interno', 'tipo_falla', 'fecha', 'informacion', 'ingreso_hs_km', 'chofer']

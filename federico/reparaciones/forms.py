from django import forms
from tablamadre.models import Reparaciones, Services, Internos

class reparaciones_form(forms.ModelForm):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Unidad de Produccion')
    ubicacion = forms.CharField(max_length=50)
    falla = forms.CharField(max_length=50)
    porcentajeavance = forms.IntegerField()
    fechareparacionestimada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fechaentrada = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fechasalida = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    estadoreparacion = forms.CharField(max_length=50)
    descripcion = forms.CharField(required=True)
    class Meta:
        model = Reparaciones
        fields = ['interno', 'ubicacion', 'falla', 'porcentajeavance', 'fechareparacionestimada', 'fechaentrada', 'fechasalida', 'estadoreparacion', 'estadoequipo']
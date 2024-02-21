from django import forms
from tablamadre.models import Consumo, Tanque, Repostaje


class ConsumoForm(forms.ModelForm):
    fecha_consumo = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Consumo
        fields = ['tanque', 'interno', 'chofer', 'consumo_litros', 'fecha_consumo', 'hskmactuales', 'precinto_entrada',
                  'precinto_salida', 'observaciones']


class CargarTanqueForm(forms.ModelForm):
    class Meta:
        model = Tanque
        fields = ['nombre', 'capacidad', 'cantidad_combustible']


class RepostajeForm(forms.ModelForm):
    class Meta:
        model = Repostaje
        fields = ['tanque', 'cantidad_litros', 'fecha', 'remito', 'proveedor']

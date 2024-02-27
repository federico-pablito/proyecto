from tablamadre.models import ConsumoAceite, TanqueAceite, RepostajeAceite
from django import forms


class ConsumoAceiteForm(forms.ModelForm):
    fecha_consumo = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = ConsumoAceite
        fields = ['id', 'tanque_aceite', 'interno', 'chofer', 'cantidad_consumida', 'fecha_consumo', 'hskmactuales', 'observaciones']

class CargarAceiteForm(forms.ModelForm):
    class Meta:
        model = TanqueAceite
        fields = ['nombre', 'tipo_aceite', 'capacidad_aceite', 'cantidad_aceite']

class RepostajeAceiteForm(forms.ModelForm):
    fecha_repostaje=forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = RepostajeAceite
        fields = ['remito', 'reservorio_aceite', 'fecha_repostaje', 'cantidad_repostada', 'observaciones']
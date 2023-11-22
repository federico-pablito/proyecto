from django import forms
from tablamadre.models import Logistica, Internos

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
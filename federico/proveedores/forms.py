from django import forms
from .models import Proveedor, EvaluacionProveedor


class ProveedorForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100, required=True)
    cuit = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    contacto = forms.CharField(max_length=100, required=True)
    activo = forms.BooleanField(required=False)

    class Meta:
        model = Proveedor
        fields = '__all__'
        exclude = ['id']


class EvaluacionProveedorForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), required=True, empty_label='Proveedor')
    fecha = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    calidad = forms.IntegerField(required=True, max_value=100, min_value=0)
    cumplimiento_plazo_entrega = forms.IntegerField(required=True, max_value=100, min_value=0)
    precio_plazo = forms.IntegerField(required=True, max_value=100, min_value=0)

    class Meta:
        model = EvaluacionProveedor
        fields = '__all__'
        exclude = ['id']

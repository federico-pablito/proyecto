from django import forms
from .models import FormOne, FormTwo, FormCombination


class FormUno(forms.ModelForm):
    fecha_requeridoobra = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    tope_requerimiento = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FormOne
        exclude = ['fecha_pedido']  # Excluye el campo no editable del formulario
        fields = ['id', 'up_solicita', 'fecha_requeridoobra', 'nivel_urgencia',
                  'repuesto', 'tipo_equipo', 'descripcion_equipo', 'motivo_requerimiento', 'tope_requerimiento']


class FormDos(forms.ModelForm):
    fecha_requeridoobra = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FormTwo
        exclude = ['fecha_pedido']
        fields = ['id', 'up_solicita', 'fecha_pedido', 'fecha_requeridoobra', 'nivel_urgencia',
                  'solicitante', 'materiales', 'descripcion']


class FormCombinacion(forms.ModelForm):
    fecha_requeridoobra = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FormCombination
        exclude = ['fecha_pedido']
        fields = ['id', 'up_solicita', 'fecha_pedido', 'fecha_requeridoobra', 'nivel_urgencia',
                  'materiales', 'repuesto', 'descripcion']


class MotivoRechazoForm(forms.Form):
    motivo = forms.CharField(label='Motivo de rechazo', widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

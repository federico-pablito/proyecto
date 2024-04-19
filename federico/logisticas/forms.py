from django import forms
from .models import FormEquipos, FormCombination, SolicitarLogistica
import json



class FormUno(forms.ModelForm):
    fecha_requeridoobra = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha requerido obra'
    )
    tope_requerimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tope De Requerimiento'
    )
    fecha_envio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha De Envio'
    )
    class Meta:
        model = FormEquipos
        fields = '__all__'  



class FormCombinacion(forms.ModelForm):
    fecha_requeridoobra = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha requerido obra'
    )
    fecha_envio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha De Envio'
    )

    id_traslado = forms.ChoiceField(choices=[], label='ID Traslado')

    class Meta:
        model = FormCombination
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        consulta_completa = kwargs.pop('consulta_completa', None)
        super(FormCombinacion, self).__init__(*args, **kwargs)
        id_choices = []
        if consulta_completa and isinstance(consulta_completa, list):
            try:
                # Agregar las opciones con el ID como value y el diccionario completo como atributo
                for item in consulta_completa:
                    id_traslado = str(item['id_traslado'])
                    label = f"{id_traslado} - {item['item_description']}"
                    id_choices.append((id_traslado, item))  # Tuple: (value, dict)

            except Exception as e:
                print(f"Error al extraer las opciones de ID: {e}")
        else:
            print("Error: El argumento consulta_completa no es una lista de diccionarios.")

        self.fields['id_traslado'].choices = id_choices
        print("Error: El argumento consulta_completa no es una lista de diccionarios.")

        self.fields['id_traslado'].choices = id_choices

    def clean_id_traslado(self):
        id_traslado = self.cleaned_data['id_traslado']
        id_choices = [choice[0] for choice in self.fields['id_traslado'].choices]
        if id_traslado not in id_choices:
            raise forms.ValidationError("ID de traslado no válido")
        return id_traslado


class FormChoice(forms.Form):
    CHOICES = [
        ('equipos', 'Formulario Equipos'),
        ('combination', 'Formulario Materiales/Repuestos')
    ]
    form_choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    

class SolicitarLogisticaForm(forms.ModelForm):
    fecha_requerido = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha requerido obra'
    )
    tope_requerimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Tope De Requerimiento'
    )
    class Meta:
        model = SolicitarLogistica
        fields = '__all__'  

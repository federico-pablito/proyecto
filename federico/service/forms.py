from django import forms
from tablamadre.models import Services, Internos

class service_form(forms.ModelForm):
    model = Services
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    fechaservicio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    fechaparte = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use the 'date' input type
    )
    ultimoservice = forms.IntegerField(required=True)
    planrealizado = forms.CharField(required=True, label='Plan Realizado (hs)')
    planrealizado_hs = forms.IntegerField(required=True, label='Plan Realizado')
    proximoservice = forms.IntegerField(required=True, label='Proximo Service')
    hsxkmactuales = forms.IntegerField(required=True, label='HrsXKm Actuales')
    operativo = forms.ChoiceField(choices=(('Operativo', 'Operativo'), ('Inoperativo', 'Inoperativo')),
                                widget=forms.Select, label='Operativo')
    class Meta:
        model = Services
        fields = ['interno', 'fechaservicio', 'fechaparte', 'ultimoservice', 'planrealizado_hs', 'planrealizado',
                'proximoservice', 'hsxkmactuales', 'operativo']

class desplegable_internos(form.Form):
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Interno')
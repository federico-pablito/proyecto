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
    hsxkmactuales = forms.IntegerField(required=True)
    descripcion = forms.CharField(required=False)
    class Meta:
        model = Services
        fields = ['interno', 'fechaservicio', 'fechaparte', 'ultimoservice', 'planrealizado_hs', 'planrealizado',
                  'proximoservice', 'hsxkmactuales', 'descripcion']

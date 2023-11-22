from django import forms
from tablamadre.models import PartesDiarios, Internos

class partediario_form(forms.ModelForm):
    model = PartesDiarios
    interno = forms.ModelChoiceField(queryset=Internos.objects.all(), empty_label=None, required=False, label='Internos')
    proveedores = forms.CharField(max_length=512, required=True, label='Proveedores')
    razonsocial = forms.CharField(max_length=512, required=True, label='Razon Social')
    cantidadequipos = forms.IntegerField(required=True, label='Cantidad de Equipos')
    kilometrajeinicial = forms.IntegerField(required=True, label='Kilometraje Inicial')
    kilometrajefinal = forms.IntegerField(required=True, label='Kilometraje Final')
    turnoreparacion = forms.CharField(max_length=512, required=True, label='Turno de Reparacion')
    horometro = forms.IntegerField(required=True, label='Horometro')
    hsxkmcarga = forms.IntegerField(required=True, label='Horas por Kilometro de Carga')
    tipocombustible = forms.CharField(max_length=512, required=True, label='Tipo de Combustible')
    tipogasoil = forms.CharField(max_length=512, required=True, label='Tipo de Gasoil')
    tiponafta = forms.CharField(max_length=512, required=True, label='Tipo de Nafta')
    litrosgasoil = forms.IntegerField(required=True, label='Litros de Gasoil')
    litrosnafta = forms.IntegerField(required=True, label='Litros de Nafta')
    tipoaceite = forms.CharField(max_length=512, required=True, label='Tipo de Aceite')
    litrosaceite = forms.IntegerField(required=True, label='Litros de Aceite')
    maquinista = forms.CharField(max_length=512, required=True, label='Maquinista')
    kmsxhs = forms.IntegerField(required=True, label='Kilometros por Hora')
    tipodefalla = forms.CharField(max_length=512, required=True, label='Tipo de Falla')
    reparado = forms.BooleanField(required=False, label='Reparado')
    class Meta:
        model = PartesDiarios
        fields = ['interno', 'proveedores', 'razonsocial', 'cantidadequipos', 'kilometrajeinicial', 'kilometrajefinal', 'turnoreparacion', 'horometro', 'hsxkmcarga', 'tipocombustible', 'tipogasoil', 'tiponafta', 'litrosgasoil', 'litrosnafta', 'tipoaceite', 'litrosaceite', 'maquinista', 'kmsxhs', 'tipodefalla', 'reparado']
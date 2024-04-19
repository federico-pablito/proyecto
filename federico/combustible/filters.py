import django_filters
from django_filters.widgets import RangeWidget
from tablamadre.models import Consumo, Repostaje, Internos, Tanque


class consumo_filter(django_filters.FilterSet):
    fecha_consumo = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    interno = django_filters.ModelChoiceFilter(field_name='interno', queryset=Internos.objects.all(), empty_label='Interno',
                                               to_field_name='interno', label='Interno')
    tanque = django_filters.ModelChoiceFilter(queryset=Tanque.objects.all(), empty_label='Tanque',
                                              label='Tanque')

    class Meta:
        model = Consumo
        fields = ['fecha_consumo', 'interno', 'tanque']


class repostaje_filter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    tanque = django_filters.ModelChoiceFilter(queryset=Tanque.objects.all(), empty_label='Tanque',
                                              label='Tanque')
    remito = django_filters.CharFilter(field_name='remito', lookup_expr='icontains')

    class Meta:
        model = Repostaje
        fields = ['fecha', 'tanque', 'remito']


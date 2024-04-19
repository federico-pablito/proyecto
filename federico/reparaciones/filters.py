import django_filters
from django_filters.widgets import RangeWidget
from tablamadre.models import UnidadesdeProduccion
from .models import Reparacion, OrdenDeReparacion, MecanicoEncargado


class reparaciones_filter(django_filters.FilterSet):
    up = django_filters.ModelChoiceFilter(field_name='interno__up__unidadproduccion',
                                          queryset=UnidadesdeProduccion.objects.all(), empty_label=None,
                                          to_field_name='unidadproduccion', label='Unidad de Produccion')

    class Meta:
        model = Reparacion
        fields = ['interno']


class ordenes_filter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr='iexact')
    fecha_creacion = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = OrdenDeReparacion
        fields = ['fecha_creacion', 'id']


class partes_filter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    mecanico_encargado = django_filters.ModelChoiceFilter(field_name='mecanico',
                                                          queryset=MecanicoEncargado.objects.all(), empty_label='Mecanico',
                                                          to_field_name='id', label='Mecanico Encargado'
                                                          )

    class Meta:
        model = OrdenDeReparacion
        fields = ['fecha', 'mecanico_encargado']

import django_filters
from django_filters.widgets import RangeWidget
from tablamadre.models import UnidadesdeProduccion
from .models import Reparacion, OrdenDeReparacion


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

import django_filters
from tablamadre.models import Reparaciones, Internos

class reparaciones_filter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr='exact', label='ID igual a')
    interno = django_filters.ModelChoiceFilter(queryset=Internos.objects.all(), to_field_name='id', empty_label=None, label='Interno igual a')
    ubicacion = django_filters.CharFilter(lookup_expr='icontains', label='Ubicacion contiene')
    falla = django_filters.CharFilter(lookup_expr='icontains', label='Falla contiene')
    porcentajeavance = django_filters.NumberFilter(lookup_expr='exact', label='Porcentaje igual a')
    fechareparacionestimada = django_filters.DateFromToRangeFilter(
        field_name='fechareparacionestimada',
        label='Fecha de Reparacion Estimada (rango)'
    )
    fechaentrada = django_filters.DateFromToRangeFilter(
        field_name='fechaentrada',
        label='Fecha de Entrada (rango)'
    )
    fechasalida = django_filters.DateFromToRangeFilter(
        field_name='fechasalida',
        label='Fecha de Salida (rango)'
    )
    estadoreparacion = django_filters.CharFilter(lookup_expr='icontains', label='Estado de Reparacion contiene')
    estadoequipo = django_filters.CharFilter(lookup_expr='icontains', label='Estado de Equipo contiene')
    class Meta:
        model = Reparaciones
        fields = {
            'id': ['exact'],
            'interno': ['exact'],
            'ubicacion': ['exact', 'icontains'],
            'falla': ['exact', 'icontains'],
            'porcentajeavance': ['exact', 'gte', 'lte'],
            'fechareparacionestimada': ['exact', 'gte', 'lte'],
            'fechaentrada': ['exact', 'gte', 'lte'],
            'fechasalida': ['exact', 'gte', 'lte'],
            'estadoreparacion': ['exact', 'icontains'],
            'estadoequipo': ['exact', 'icontains'],
        }
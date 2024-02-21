import django_filters
from tablamadre.models import Internos, UnidadesdeProduccion

class internosfilter(django_filters.FilterSet):
    interno = django_filters.CharFilter(lookup_expr='icontains')
    up = django_filters.ModelChoiceFilter(queryset=UnidadesdeProduccion.objects.all(), to_field_name='id', empty_label=None, label='Unidad de Produccion')
    marca = django_filters.CharFilter(lookup_expr='icontains')
    modelo = django_filters.CharFilter(lookup_expr='icontains')
    dominio = django_filters.CharFilter(lookup_expr='icontains')
    actividadvehiculo = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Internos
        fields = {
            'interno': ['exact', 'icontains'],
            'up': ['exact'],
            'marca': ['icontains'],
            'modelo': ['icontains'],
            'dominio': ['icontains'],
            'actividadvehiculo': ['exact'],
        }


class alquilerfilter(django_filters.FilterSet):
    interno = django_filters.CharFilter(lookup_expr='icontains')
    up = django_filters.ModelChoiceFilter(queryset=UnidadesdeProduccion.objects.all(), to_field_name='id', empty_label=None, label='Unidad de Produccion')
    marca = django_filters.CharFilter(lookup_expr='icontains')
    modelo = django_filters.CharFilter(lookup_expr='icontains')
    dominio = django_filters.CharFilter(lookup_expr='icontains')
    actividadvehiculo = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Internos
        fields = {
            'interno': ['exact', 'icontains'],
            'up': ['exact'],
            'marca': ['icontains'],
            'modelo': ['icontains'],
            'dominio': ['icontains'],
            'actividadvehiculo': ['exact'],
        }

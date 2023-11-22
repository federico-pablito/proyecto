import django_filters
from tablamadre.models import Internos, UnidadesdeProduccion

class internosfilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr='iexact')
    interno = django_filters.CharFilter(lookup_expr='icontains')
    up = django_filters.ModelChoiceFilter(queryset=UnidadesdeProduccion.objects.all(), to_field_name='id', empty_label=None, label='Unidad de Produccion')
    marca = django_filters.CharFilter(lookup_expr='icontains')
    modelo = django_filters.CharFilter(lookup_expr='icontains')
    chasis = django_filters.CharFilter(lookup_expr='icontains')
    motor = django_filters.CharFilter(lookup_expr='icontains')
    anio = django_filters.NumberFilter(lookup_expr='exact')
    aseguradora = django_filters.CharFilter(lookup_expr='icontains')
    seguro = django_filters.CharFilter(lookup_expr='icontains')
    seguro_pdf = django_filters.CharFilter(lookup_expr='icontains')
    itv = django_filters.CharFilter(lookup_expr='icontains')
    itv_pdf = django_filters.CharFilter(lookup_expr='icontains')
    titulo_pdf = django_filters.CharFilter(lookup_expr='icontains')
    tarjeta = django_filters.CharFilter(lookup_expr='icontains')
    tarjeta_pdf = django_filters.CharFilter(lookup_expr='icontains')
    propietario = django_filters.CharFilter(lookup_expr='icontains')
    chofer = django_filters.CharFilter(lookup_expr='icontains')
    alquilado = django_filters.BooleanFilter(lookup_expr='exact')
    valorpesos = django_filters.NumberFilter(lookup_expr='exact')
    valordolares = django_filters.NumberFilter(lookup_expr='exact')
    orden = django_filters.CharFilter(lookup_expr='icontains')
    actividadvehiculo = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Internos
        fields = {
            'interno': ['exact', 'icontains'],
            'up': ['exact'],
            'marca': ['exact', 'icontains'],
            'modelo': ['exact', 'icontains'],
            'chasis': ['exact', 'icontains'],
            'motor': ['exact', 'icontains'],
            'anio': ['exact', 'gte', 'lte'],
            'aseguradora': ['exact', 'icontains'],
            'seguro': ['exact', 'icontains'],
            'itv': ['exact', 'icontains'],
            'propietario': ['exact', 'icontains'],
            'chofer': ['exact', 'icontains'],
            'alquilado': ['exact'],
            'valorpesos': ['exact', 'gte', 'lte'],
            'valordolares': ['exact', 'gte', 'lte'],
            'orden': ['exact', 'icontains'],
            'actividadvehiculo': ['exact', 'icontains'],
        }

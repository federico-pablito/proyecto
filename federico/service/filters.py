import django_filters
from tablamadre.models import Services, UnidadesdeProduccion


class servicefilter(django_filters.FilterSet):
    up = django_filters.ModelChoiceFilter(field_name='interno__up__unidadproduccion', queryset=UnidadesdeProduccion.objects.all(),
                                          to_field_name='unidadproduccion', empty_label=None, label='Unidad de Produccion')

    class Meta:
        model = Services
        fields = ['interno']
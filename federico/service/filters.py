import django_filters
from tablamadre.models import Services, UnidadesdeProduccion, Internos


class servicefilter(django_filters.FilterSet):
    up = django_filters.ModelChoiceFilter(field_name='interno__up__unidadproduccion', queryset=UnidadesdeProduccion.objects.all(),
                                          to_field_name='unidadproduccion', empty_label='UP', label='Unidad de Produccion')
    interno = django_filters.ModelChoiceFilter(field_name='interno__interno', queryset=Internos.objects.all(),
                                          to_field_name='interno', empty_label='Interno', label='Internos')
    class Meta:
        model = Services
        fields = ['interno']

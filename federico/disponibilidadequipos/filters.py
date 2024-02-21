import django_filters
from tablamadre.models import DisponibilidadEquipos, UnidadesdeProduccion


class disponibilidadfilter(django_filters.FilterSet):
    up = django_filters.ModelChoiceFilter(queryset=UnidadesdeProduccion.objects.all(), to_field_name='id', empty_label=None, label='Unidad de Produccion')

    class Meta:
        model = DisponibilidadEquipos
        fields = {
            'up': ['exact'],
        }

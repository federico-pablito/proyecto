import django_filters
from tablamadre.models import Services, Internos


class service_filter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr='exact', label='ID igual a')
    interno = django_filters.ModelChoiceFilter(queryset=Internos.objects.all(), to_field_name='id', empty_label=None,
                                               label='Interno igual a')
    fechaservicio = django_filters.DateFromToRangeFilter(
        field_name='fechaservicio',
        label='Fecha de Servicio (rango)'
    )

    fechaparte = django_filters.DateFromToRangeFilter(
        field_name='fechaparte',
        label='Fecha de Parte (rango)'
    )
    class Meta:
        model = Services
        fields = {
            'interno': ['exact'],
            'fechaservicio': ['exact', 'gte', 'lte'],
            'fechaparte': ['exact', 'gte', 'lte'],
            'ultimoservice': ['exact', 'gte', 'lte'],
            'planrealizado_hs': ['exact', 'gte', 'lte'],
            'planrealizado': ['icontains'],
            'proximoservice': ['exact', 'gte', 'lte'],
            'hsxkmactuales': ['exact', 'gte', 'lte'],
        }

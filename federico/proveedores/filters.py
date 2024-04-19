import django_filters
from django_filters.widgets import RangeWidget
from .models import Proveedor, EvaluacionProveedor


class EvaluacionFilter(django_filters.FilterSet):
    proveedor = django_filters.ModelChoiceFilter(queryset=Proveedor.objects.all(), label='Proveedor',
                                                 empty_label='Todos')
    fecha = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = EvaluacionProveedor
        fields = ['proveedor', 'fecha']
import django_filters
from django_filters.widgets import RangeWidget
from tablamadre.models import ConsumoAceite, RepostajeAceite, Internos, TanqueAceite


class consumo_filter(django_filters.FilterSet):
    fecha_consumo = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    interno = django_filters.ModelChoiceFilter(queryset=Internos.objects.all(), empty_label='Interno',
                                               to_field_name='interno', label='Interno')
    tanque_aceite = django_filters.ModelChoiceFilter(queryset=TanqueAceite.objects.all(), empty_label='Tanque',
                                                label='Tanque')

    class Meta:
        model = ConsumoAceite
        fields = ['fecha_consumo', 'interno', 'tanque_aceite']


class repostaje_filter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    reservorio_aceite = django_filters.ModelChoiceFilter(queryset=TanqueAceite.objects.all(), empty_label='Tanque',
                                                label='Tanque')
    remito = django_filters.CharFilter(field_name='remito', lookup_expr='icontains')

    class Meta:
        model = RepostajeAceite
        fields = ['fecha', 'reservorio_aceite', 'remito']


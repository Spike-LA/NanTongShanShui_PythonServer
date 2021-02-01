import django_filters

from App.models import Pump


class PumpFilter(django_filters.FilterSet):
    pump_code = django_filters.CharFilter(field_name='pump_code',lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:

        model = Pump

        fields = []
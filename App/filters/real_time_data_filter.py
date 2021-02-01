import django_filters

from App.models import RealTimeData


class RealTimeDataFilter(django_filters.FilterSet):
    equipment_code = django_filters.CharFilter(field_name='equipment_code', lookup_expr='exact')

    class Meta:

        model = RealTimeData

        fields = []
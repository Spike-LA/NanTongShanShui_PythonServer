import django_filters
from django_filters.rest_framework import FilterSet

from App.models import MainEngine


class MainEngineFilter(FilterSet):
    engine_code = django_filters.CharFilter(field_name='engine_code', lookup_expr='exact')
    begin_time_gte = django_filters.DateFilter(field_name='begin_time', lookup_expr='gte')
    begin_time_lte = django_filters.DateFilter(field_name='begin_time', lookup_expr='lte')
    end_time_gte = django_filters.DateFilter(field_name='end_time', lookup_expr='gte')
    end_time_lte = django_filters.DateFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = MainEngine
        fields = []

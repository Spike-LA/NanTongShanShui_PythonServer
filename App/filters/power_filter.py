import django_filters
from django_filters.rest_framework import FilterSet

from App.models import Power


class PowerFilter(FilterSet):
    power = django_filters.CharFilter(field_name='power', lookup_expr='exact')

    class Meta:
        model = Power
        fields = []

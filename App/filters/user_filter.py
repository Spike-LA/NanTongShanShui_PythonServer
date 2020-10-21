import django_filters

from App.models import User


class UserFilter(django_filters.FilterSet):
    account = django_filters.CharFilter(field_name='account', lookup_expr='icontains')
    role_id = django_filters.CharFilter(field_name='role_id', lookup_expr='exact')
    mod_by = django_filters.CharFilter(field_name='mod_by', lookup_expr='icontains')
    add_time_gte = django_filters.DateFilter(field_name='add_time', lookup_expr='gte')
    add_time_lte = django_filters.DateFilter(field_name='add_time', lookup_expr='lte')
    mod_time_get = django_filters.DateFilter(field_name='mod_time', lookup_expr='gte')
    mod_time_lte = django_filters.DateFilter(field_name='mod_time', lookup_expr='lte')

    class Meta:
        model = User
        fields = []


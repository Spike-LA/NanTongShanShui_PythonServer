import django_filters

from App.models import CustomerAccount


class CustomerAccountFilter(django_filters.FilterSet):
    account_id = django_filters.CharFilter(field_name='account_id', lookup_expr='icontains')
    account_number = django_filters.CharFilter(field_name='account_number', lookup_expr='icontains')
    add_by = django_filters.CharFilter(field_name='add_by', lookup_expr='icontains')
    mod_by = django_filters.CharFilter(field_name='mod_by', lookup_expr='icontains')
    add_time_lte = django_filters.DateFilter(field_name='add_time', lookup_expr='lte')  # 创建时间最大值
    add_time_gte = django_filters.DateFilter(field_name='add_time', lookup_expr='gte')  # 创建时间最小值
    mod_time_lte = django_filters.DateFilter(field_name='mod_time', lookup_expr='lte')  # 修改时间最大值
    mod_time_gte = django_filters.DateFilter(field_name='mod_time', lookup_expr='gte')  # 修改时间最小值

    class Meta:
        model = CustomerAccount
        fields = []

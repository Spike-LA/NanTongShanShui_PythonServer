import django_filters

from App.models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    engine_code = django_filters.CharFilter(field_name="engine_code", lookup_expr='exact')  # 精确查询
    equipment_code = django_filters.CharFilter(field_name="equipment_code", lookup_expr='exact')
    begin_date = django_filters.DateTimeFilter(field_name="alert_time", lookup_expr='gte')  # 大于等于
    last_date = django_filters.DateTimeFilter(field_name="alert_time", lookup_expr='lte')  # 小于等于
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')

    class Meta:

        model = Equipment

        fields = ['engine_code']

import django_filters

from App.models import EquipmentOperationLog


class EquipmentOperationLogFilter(django_filters.FilterSet):
    equipment_code = django_filters.CharFilter(field_name="operation_equipment_code", lookup_expr='exact')
    pump_code = django_filters.CharFilter(field_name="operation_pump_code", lookup_expr='exact')
    operation_time_gte = django_filters.DateFilter(field_name='operation_time', lookup_expr='gte')
    operation_time_lte = django_filters.DateFilter(field_name='operation_time', lookup_expr='lte')
    operate_status = django_filters.CharFilter(field_name="operate_status", lookup_expr='exact')

    class Meta:
        model = EquipmentOperationLog

        fields = []
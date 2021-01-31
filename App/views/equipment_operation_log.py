from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from App.filters.equipment_operation_log_filter import EquipmentOperationLogFilter
from App.models import EquipmentOperationLog
from App.pagination import MyPageNumberPagination
from App.serializers.equipment_operation_log_serializer import EquipmentOperationLogSerializer


class EquipmentOperationLogViewSet(viewsets.ModelViewSet):
    queryset = EquipmentOperationLog.objects.all()
    serializer_class = EquipmentOperationLogSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = EquipmentOperationLogFilter
    pagination_class = MyPageNumberPagination
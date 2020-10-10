from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.models import EquipmentMaintenance
from App.pagination import MyPageNumberPagination
from App.serializers.equipment_maintenance_serializer import EquipmentMaintenanceSerializer


class EquipmentMaintenanceViewSet(ModelViewSet,):
    queryset = EquipmentMaintenance.objects.all()
    serializer_class = EquipmentMaintenanceSerializer

    # 用于查询集过滤的过滤器后端类
    filter_backends = (DjangoFilterBackend,)
    # filter_class = MainEngineFilter
    pagination_class = MyPageNumberPagination






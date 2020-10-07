from rest_framework.viewsets import ModelViewSet

from App.models import EquipmentMaintenance
from App.serializers.equipment_maintenance import EquipmentMaintenanceSerializer


class EquipmentMaintenanceViewSet(ModelViewSet):
    queryset = EquipmentMaintenance.objects.all()
    serializer_class = EquipmentMaintenanceSerializer

from rest_framework.viewsets import ModelViewSet

from App.models import EquipmentAllocation
from App.serializers.equipment_allocation_serializer import EquipmentAllocationSerializer


class EquipmentAllocationViewSet(ModelViewSet):

    queryset = EquipmentAllocation.objects.all()
    serializer_class = EquipmentAllocationSerializer


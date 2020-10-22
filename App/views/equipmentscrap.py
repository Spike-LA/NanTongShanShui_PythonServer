from rest_framework import viewsets

from App.models import EquipmentScrap
from App.serializers.equipmentscrap_serializer import EquipmentScrapSerializer


class EquipmentScrapViewSet(viewsets.ModelViewSet):
    queryset = EquipmentScrap.objects.all()
    serializer_class = EquipmentScrapSerializer

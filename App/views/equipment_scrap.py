
from rest_framework.viewsets import ModelViewSet

from App.models import EquipmentScrap
from App.serializers.equipment_scrap_serializer import EquipmentScrapSerializer


class EquipmentScrapViewSet(ModelViewSet):

    queryset = EquipmentScrap.objects.all()
    serializer_class = EquipmentScrapSerializer


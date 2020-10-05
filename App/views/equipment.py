from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from App.filters.equipment_filter import EquipmentFilter
from App.models import Equipment
from App.serializers.equipment_serializer import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = EquipmentFilter

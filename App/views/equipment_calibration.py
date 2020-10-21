from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.models import SensorCalibration
from App.pagination import MyPageNumberPagination
from App.serializers.equipment_calibration_serializer import EquipmentCalibrationSerializer


class EquipmentCalibrationViewSet(ModelViewSet):

    queryset = SensorCalibration.objects.all()
    serializer_class = EquipmentCalibrationSerializer

    filter_backends = (DjangoFilterBackend,)
    pagination_class = MyPageNumberPagination

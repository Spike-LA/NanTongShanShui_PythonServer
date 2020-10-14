import pymysql
from rest_framework import viewsets

from App.models import SensorType
from App.serializers.sensor_type_serializer import SensorTypeSerializer


class SensorTypeViewSet(viewsets.ModelViewSet):

    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer


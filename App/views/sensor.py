from rest_framework import viewsets

from App.models import Sensor
from App.serializers.sensor_serializer import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


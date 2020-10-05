from rest_framework import viewsets

from App.models import SensorModel
from App.serializers.sensor_model_serializer import SensorModelSerializer


class SensorModelViewSet(viewsets.ModelViewSet):

    queryset = SensorModel.objects.all()
    serializer_class = SensorModelSerializer

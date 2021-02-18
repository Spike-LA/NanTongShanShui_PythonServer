from rest_framework import viewsets

from App.models import SensorType
from App.serializers.sensor_type_serializer import SensorTypeSerializer
from App.views_constant import Delete


class SensorTypeViewSet(viewsets.ModelViewSet):

    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.state = Delete
        instance.save()

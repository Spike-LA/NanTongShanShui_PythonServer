from rest_framework import viewsets

from App.models import SensorModel
from App.serializers.sensor_model_serializer import SensorModelSerializer
from App.views_constant import Delete


class SensorModelViewSet(viewsets.ModelViewSet):

    queryset = SensorModel.objects.all()
    serializer_class = SensorModelSerializer

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.states = Delete
        instance.save()

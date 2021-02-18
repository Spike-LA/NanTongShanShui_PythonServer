from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from App.filters.real_time_data_filter import RealTimeDataFilter
from App.models import RealTimeData
from App.serializers.real_time_data import RealTimeDataSerializer


class RealTimeDataViewSet(viewsets.ModelViewSet):
    queryset = RealTimeData.objects.all()
    serializer_class = RealTimeDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = RealTimeDataFilter
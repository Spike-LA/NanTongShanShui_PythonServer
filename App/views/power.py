from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.filters.power_filter import PowerFilter
from App.serializers.power_serializer import PowerSerializer
from App.models import Power


class PowerViewSet(ModelViewSet):

    queryset = Power.objects.all()
    serializer_class = PowerSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = PowerFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from App.filters.pump_filter import PumpFilter
from App.models import Pump
from App.pagination import MyPageNumberPagination
from App.serializers.pump_serializer import PumpSerializer
from App.views_constant import is_delete


class PumpViewSet(viewsets.ModelViewSet):
    queryset = Pump.objects.all()
    serializer_class = PumpSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = PumpFilter
    pagination_class = MyPageNumberPagination

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.status = is_delete
        instance.save()
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from App.filters.auto_operation_filter import AutoOperationFilter
from App.models import AutoOperationInfo
from App.pagination import MyPageNumberPagination
from App.serializers.auto_operation_serializer import AutoOperationSerializer


class AutoOperationViewSet(viewsets.ModelViewSet):
    queryset = AutoOperationInfo.objects.all()
    serializer_class = AutoOperationSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = AutoOperationFilter
    pagination_class = MyPageNumberPagination


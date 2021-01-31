from rest_framework import viewsets

from App.models import PumpPermission
from App.pagination import MyPageNumberPagination
from App.serializers.pump_permission_serializer import PumpPermissionSerializer


class PumpPermissionViewSet(viewsets.ModelViewSet):
    queryset = PumpPermission.objects.all()
    serializer_class = PumpPermissionSerializer

    pagination_class = MyPageNumberPagination
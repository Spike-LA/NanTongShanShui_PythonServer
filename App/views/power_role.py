from rest_framework import viewsets

from App.models import PowerRole
from App.serializers.power_role_serializer import PowerRoleSerializer


class PowerRoleViewSet(viewsets.ModelViewSet):
    queryset = PowerRole.objects.all()
    serializer_class = PowerRoleSerializer
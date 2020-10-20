from rest_framework import viewsets

from App.models import Role
from App.serializers.role_serializer import RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

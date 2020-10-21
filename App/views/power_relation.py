from rest_framework import viewsets

from App.models import PowerRelation
from App.serializers.power_relation_serializer import PowerRelationSerializer


class PowerRelationViewSet(viewsets.ModelViewSet):
    queryset = PowerRelation.objects.all()
    serializer_class = PowerRelationSerializer

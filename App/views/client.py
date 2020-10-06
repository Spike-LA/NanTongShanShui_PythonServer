from rest_framework import viewsets

from App.models import Client
from App.serializers.client_serializer import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

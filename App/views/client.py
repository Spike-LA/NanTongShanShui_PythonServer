from rest_framework import viewsets

from App.models import Client
from App.pagination import MyPageNumberPagination
from App.serializers.client_serializer import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    pagination_class = MyPageNumberPagination

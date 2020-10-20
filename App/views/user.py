from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.models import User
from App.pagination import MyPageNumberPagination
from App.serializers.user_serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(status=1)
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend,)
    pagination_class = MyPageNumberPagination

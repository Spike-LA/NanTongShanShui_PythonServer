from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.filters.user_filter import UserFilter
from App.models import User
from App.pagination import MyPageNumberPagination
from App.serializers.user_serializer import UserSerializer
from App.views_constant import Delete


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(status=1)
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend,)
    pagination_class = MyPageNumberPagination
    filter_class = UserFilter

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.status = Delete
        instance.save()

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.filters.enterprise_account_filter import EnterpriseAccountFilter
from App.models import EnterpriseAccount
from App.pagination import MyPageNumberPagination
from App.serializers.enterprise_account_serializer import EnterpriseAccountSerializer


class EnterpriseAccountViewSet(ModelViewSet):
    queryset = EnterpriseAccount.objects.all()
    serializer_class = EnterpriseAccountSerializer

    # 用于查询集过滤的过滤器后端类
    filter_backends = (DjangoFilterBackend,)
    filter_class = EnterpriseAccountFilter
    pagination_class = MyPageNumberPagination

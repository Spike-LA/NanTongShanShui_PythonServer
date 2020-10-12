from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.filters.customer_account_filter import CustomerAccountFilter
from App.models import CustomerAccount
from App.pagination import MyPageNumberPagination
from App.serializers.customer_account_serializer import CustomerAccountSerializer


class CustomerAccountViewSet(ModelViewSet):
    queryset = CustomerAccount.objects.all()
    serializer_class = CustomerAccountSerializer

    # 用于查询集过滤的过滤器后端类
    filter_backends = (DjangoFilterBackend,)
    filter_class = CustomerAccountFilter
    pagination_class = MyPageNumberPagination

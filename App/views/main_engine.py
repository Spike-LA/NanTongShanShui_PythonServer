from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.filters.main_engine_filter import MainEngineFilter
from App.models import MainEngine
from App.pagination import MyPageNumberPagination
from App.serializers.main_engine_serializer import MainEngineSerializer

from App.views_constant import Delete


class MainEngineViewSet(ModelViewSet):
    serializer_class = MainEngineSerializer
    queryset = MainEngine.objects.exclude(status=-1)

    # 用于查询集过滤的过滤器后端类
    filter_backends = (DjangoFilterBackend,)
    filter_class = MainEngineFilter
    pagination_class = MyPageNumberPagination

    # 改写原来的删除函数，使其变为假删
    def perform_destroy(self, instance):
        instance.status = Delete
        instance.save()

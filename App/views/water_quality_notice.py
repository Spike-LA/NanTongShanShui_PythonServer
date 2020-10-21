from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from App.models import WaterQualityNotice
from App.pagination import MyPageNumberPagination
from App.serializers.water_quality_notice_serializer import WaterQualityNoticeSerializer


class WaterQualityNoticeViewSet(ModelViewSet):
    queryset = WaterQualityNotice.objects.all()
    serializer_class = WaterQualityNoticeSerializer

    filter_backends = (DjangoFilterBackend,)
    pagination_class = MyPageNumberPagination

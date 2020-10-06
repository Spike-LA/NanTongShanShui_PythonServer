from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from App.models import MainEngine
from App.serializers.pagination_serializer import PagerSerializer


class MyPageNumberPagination(PageNumberPagination):  # main_engine分页
    page_size = 5
    max_page_size = 40
    page_size_query_param = 'size'
    page_query_param = 'page'


class PageView(APIView):  # main_engine分页
    def get(self, request, *args, **kwargs):
        engines = MainEngine.objects.get_queryset().order_by('aid')
        page = MyPageNumberPagination()
        page_roles = page.paginate_queryset(queryset=engines, request=request, view=self)
        roles_ser = PagerSerializer(instance=page_roles, many=True)

        num = engines.count()

        data = {
            "count": num,
            "data": roles_ser.data
        }

        return Response(data=data)  # 只返回数据
        # return page.get_paginated_response(roles_ser.data)  # 返回前后夜url

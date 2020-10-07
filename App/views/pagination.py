from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):  # 自定义分页器，定义之后在类视图中进行调用可供所有的类视图使用。
    page_size = 5  # 后端指定每页显示数量
    max_page_size = 40  # 后端指定每页最大显示数量
    page_size_query_param = 'size'
    page_query_param = 'currentPage'

    def get_paginated_response(self, data):  # # 重写分页返回方法，按照指定的字段进行分页数据返回

        return Response({
            'count': self.page.paginator.count,  # 总数量
            'results': data,  # 用户数据
            # 'page' : self.page.number, # 当前页数
            # 'pages' : self.page.paginator.num_pages, # 总页数
            # 'pagesize':self.page_size  # 后端指定的页容量
        })


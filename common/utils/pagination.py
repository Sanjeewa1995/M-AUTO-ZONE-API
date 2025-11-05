from rest_framework.pagination import PageNumberPagination
from common.utils import APIResponse
from rest_framework import status


class CustomPageNumberPagination(PageNumberPagination):
    """
        Custom pagination that returns APIResponse format
        """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return APIResponse.success(
            data=data,
            message='Data retrieved successfully',
            meta={
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                    'current_page': self.page.number,
                    'total_pages': self.page.paginator.num_pages
            }
        )

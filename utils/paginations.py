from rest_framework import pagination
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class CommonPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'pageSize'
    invalid_page_message = _("Invalid page")

    def get_paginated_response(self, data):
        self.page_size = int(self.request.query_params.get(self.page_size_query_param, self.page_size))

        return Response({
            'currentPage': self.page.number,
            "countItemsOnPage": self.page.count(self.page.number),
            'totalPages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'pageSize': self.page_size,
            'results': data
        })

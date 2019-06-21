from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict

class PageNumberPagination(PageNumberPagination):
    page_size = 10
    #page_size_query_param = 'limit'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
        
class LimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
        
class DatatablesPagination(LimitOffsetPagination):
    # limit_query_param = 'length'
    # offset_query_param = 'start'
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('recordsFiltered', self.count),
            ('data', data)
        ]))
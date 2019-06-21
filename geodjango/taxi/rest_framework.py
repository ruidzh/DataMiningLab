from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.core.cache import cache

class PageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
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

def _get_count(queryset):
    """
    Determine an object count, supporting either querysets or regular lists.
    """
    # try:
    import hashlib
    key = hashlib.md5(str(queryset.query).split("FROM",1)[1].encode('utf-8')).hexdigest()
    count = cache.get(key)
    if count is None:
        def count_daemon():
            count = queryset.count()
            cache.set(key,count,72*3600) #timeout 3 days
        import threading
        thread = threading.Thread(target=count_daemon, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()
        return 100
    return count
    # except (AttributeError, TypeError):
        # print('error')
        # return 10#len(queryset)
        
class DatatablesPagination(LimitOffsetPagination):
    # limit_query_param = 'length'
    # offset_query_param = 'start'
    max_limit = 10000
    def paginate_queryset(self, queryset, request, view=None):
        self.count = _get_count(queryset)
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        # print(self.__dict__.keys())
        # for k,v in queryset.__dict__.items():
            # print(k)
            # print(v)
        res = list(queryset[self.offset:self.offset + self.limit])
        # for r in res:
            # print(r.__dict__.keys())
        return res
        
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('recordsFiltered', self.count),
            ('data', data)
        ]))
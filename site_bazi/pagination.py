import math

from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response
from django.core.paginator import Paginator as DjangoPaginator

class PaginationWithCount(pagination.LimitOffsetPagination):
    # num_pages = 0
    # django_paginator_class = DjangoPaginator
    # def paginate_queryset(self, queryset, request, view=None):
    #     r = super().paginate_queryset(queryset, request)
    #     paginator = self.django_paginator_class(queryset, self.limit)
    #     self.num_pages = paginator.num_pages
    #     return r

    def get_paginated_response(self, data):
        res = super().get_paginated_response(data)
        res.data['num_pages'] = math.ceil(self.count/self.limit)
        res.data.move_to_end('num_pages', last = False)
        return res

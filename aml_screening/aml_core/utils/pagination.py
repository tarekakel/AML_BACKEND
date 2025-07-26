# pagination.py
from rest_framework.pagination import PageNumberPagination

class CustomPageSizePagination(PageNumberPagination):
    # default page size if no pageSize in the query string
    page_size = 10
    # the name of our “perPage” override param
    page_size_query_param = 'pageSize'
    # maximum pageSize a client can request
    max_page_size = 100
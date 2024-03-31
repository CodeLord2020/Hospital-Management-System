from rest_framework.pagination import PageNumberPagination

class patients_paginator(PageNumberPagination):
    page_size = 10

class appointmennt_paginator(PageNumberPagination):
    page_size = 2
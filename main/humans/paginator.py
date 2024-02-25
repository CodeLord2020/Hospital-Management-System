from rest_framework.pagination import PageNumberPagination

class patients_paginator(PageNumberPagination):
    page_size = 10
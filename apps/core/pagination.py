"""
Custom pagination classes for the API.
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class with customizable page size.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Pagination class for endpoints that need to return more results.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500

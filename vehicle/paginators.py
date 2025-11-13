from rest_framework.pagination import PageNumberPagination


class VehiclePaginator(PageNumberPagination):
    page_size = 5

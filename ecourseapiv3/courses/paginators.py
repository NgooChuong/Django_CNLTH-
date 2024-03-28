from rest_framework import pagination


class Item_Paginations(pagination.PageNumberPagination):
    page_size = 2

from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework import status

class BasePagination(CursorPagination):
    ordering = "-created_at"

    def get_paginated_response(self, data):
        return Response({
            "status_code": status.HTTP_200_OK,
            "success": True,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data
        }, status=status.HTTP_200_OK)
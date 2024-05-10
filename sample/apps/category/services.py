from apps.core.models import APIResponse
from rest_framework import status

class CategoryServiceMixin:
    def get_categories(self):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
    def create_category(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
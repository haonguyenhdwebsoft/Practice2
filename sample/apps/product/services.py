from apps.core.models import APIResponse
from rest_framework import status

class ProductServiceMixin:
    def get_products(self):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
    def create_product(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
    
    def get_product(self):
        product = self.get_object()
        serializer = self.serializer_class(product)
        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
    def update_product(self, data):
        product = self.get_object()
        serializer = self.serializer_class(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
    def delete_product(self):
        product = self.get_object()
        product.delete()
        return APIResponse(status_code=status.HTTP_200_OK, success=True, data={})
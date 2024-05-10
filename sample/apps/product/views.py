from django.shortcuts import render
from rest_framework import generics, status
from .models import Product
from .serializers import ProductSerializer
from .renderers import ProductJSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import ProductServiceMixin

# Create your views here.
class ProductListCreateAPIView(ProductServiceMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (ProductJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.id).prefetch_related("categories")
    
    def list(self, request, *args, **kwargs):
        api_response = self.get_products()
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        api_response = self.create_product(data)
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)

class ProductRetrieveUpdateDestroyAPIView(ProductServiceMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (ProductJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.id)
    
    def retrieve(self, request, *args, **kwargs):
        api_response = self.get_product()
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        api_response = self.update_product(request.data)
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        api_response = self.delete_product()
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
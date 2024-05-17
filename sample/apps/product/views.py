from django.shortcuts import render
from rest_framework import generics, status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .renderers import ProductJSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.core.models import APIResponse
from .tasks import notify_user
from django.db import transaction

# Create your views here.
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = (ProductJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        api_response = APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (ProductJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.id).prefetch_related("categories")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        with transaction.atomic():
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            transaction.on_commit(lambda: notify_user.delay(request.user.email))
        api_response = APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = (ProductJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.id)
    
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(product)
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        with transaction.atomic():
            serializer = self.serializer_class(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data={})
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
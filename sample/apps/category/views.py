from django.shortcuts import render
from rest_framework import generics, status
from .models import Category
from .serializers import CategorySerializer
from .renderers import CategoryJSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import CategoryServiceMixin
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class CategoryListCreateAPIView(CategoryServiceMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = (CategoryJSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        api_response = self.get_categories()
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        api_response = self.create_category(request.data)
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
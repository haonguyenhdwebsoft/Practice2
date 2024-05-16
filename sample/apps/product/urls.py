from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView

urlpatterns = [
    path("categories", CategoryListCreateAPIView.as_view()),
    path("products", ProductListCreateAPIView.as_view()),
    path("products/<int:pk>", ProductRetrieveUpdateDestroyAPIView.as_view())
]
from rest_framework import serializers
from .models import Product
from .models import Category
from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    
    class Meta:
        model = Product
        fields = ["id", "name", "categories", "user"]
    
    def create(self, validated_data):
        categories = validated_data.pop("categories")
        product = Product.objects.create(**validated_data)
        product.categories.add(*categories)
        return product
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        categories = validated_data.get("categories", [])
        if len(categories) > 0:
            instance.categories.clear()
            instance.categories.add(*categories)
        instance.save()
        return instance
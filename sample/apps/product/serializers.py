from rest_framework import serializers
from .models import Product
from apps.category.serializers import CategorySerializer
from .models import Category
from apps.authentication.serializers import UserSerializer
from apps.authentication.models import User

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    
    class Meta:
        model = Product
        fields = ["id", "name", "categories", "user"]
    
    def create(self, validated_data):
        categories = validated_data.pop("categories")
        product = Product.objects.create(**validated_data)
        for category in categories:
            product.categories.add(category)
        return product
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        categories = validated_data.get("categories", [])
        if len(categories) > 0:
            instance.categories.clear()
            for category in categories:
                instance.categories.add(category)
        instance.save()
        return instance
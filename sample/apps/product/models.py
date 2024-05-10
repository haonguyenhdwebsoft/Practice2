from django.db import models
from apps.category.models import Category
from apps.authentication.models import User
from apps.core.models import TimestampedModel

# Create your models here.
class Product(TimestampedModel):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
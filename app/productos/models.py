from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=254)
    user_obj=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class SubCategory(models.Model):
    name=models.CharField(max_length=254)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

class Producto(models.Model):
    name =models.CharField(max_length=200, blank=True, null=True)
    description=models.CharField(max_length=200, blank=True, null=True)
    user_obj=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    unit_price=models.FloatField()
    sub_categoria=models.ForeignKey(SubCategory, on_delete=models.CASCADE,)

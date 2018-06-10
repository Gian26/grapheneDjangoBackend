from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title=models.CharField(max_length=100, unique=True)
    slug=models.CharField(max_length=100, unique=True)
    body=models.TextField()
    publish_date=models.DateField(db_index=True, auto_now_add=False)
    public=models.BooleanField(default=False)
    user_obj=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    task = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=50)

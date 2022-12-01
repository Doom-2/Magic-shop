from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(unique=True, max_length=10, null=True, validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = [
        ("admin", "Администратор"),
        ("moderator", "Модератор"),
        ("member", "Участник")
    ]

    role = models.CharField(max_length=15, choices=ROLES, default="member")
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    locations = models.ManyToManyField(Location, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username

    @property
    def total_ads(self):
        return self.ads.filter(is_published=True).count()


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name='ads', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=2000)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-price"]

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(User, related_name='selections', on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self):
        return self.name

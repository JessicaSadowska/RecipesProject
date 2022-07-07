from django.contrib.auth.models import User
from django.db import models


class Allergen(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=100)
    ingredients = models.TextField()
    preparation = models.TextField()
    kcal = models.IntegerField()
    proteins = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    allergens = models.ManyToManyField(Allergen, related_name="allergens_list", default=None)
    category = models.ManyToManyField(Category, related_name="category", default=None)
    image = models.ImageField(default='../static/brakzdjecia.png')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Diet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    kcal = models.IntegerField
    meals = models.ManyToManyField(Recipe, related_name="meals_list")



from django.db import models


class Allergen(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    kcal = models.IntegerField()
    proteins = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    allergens = models.ManyToManyField(Allergen, related_name="list_of_allergens", default=None)
    image = models.ImageField()



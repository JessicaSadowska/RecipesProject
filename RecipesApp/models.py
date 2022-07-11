from django.contrib.auth.models import User
from django.db import models


class Allergen(models.Model):
    """
    Stores a single allergen.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Stores a single category.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Stores a single recipe, related to :model:`Allergen`, :model:`Category`
    and :model:`auth.User`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    ingredients = models.TextField()
    preparation = models.TextField()
    kcal = models.IntegerField()
    proteins = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    allergens = models.ManyToManyField(Allergen, related_name="allergens_list", default=None, blank=True)
    category = models.ManyToManyField(Category, related_name="category", default=None, blank=True)
    image = models.ImageField(default='../static/brakzdjecia.png')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Diet(models.Model):
    """
    Stores a single diet, related to :model:`Recipe` and
    :model:`auth.User`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    meals = models.ManyToManyField(Recipe, related_name="meals_list")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Opinion(models.Model):
    """
    Stores a single opinion, related to :model:`Recipe`
    and :model:`auth.User`.
    """
    RATINGS = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(choices=RATINGS, default=5)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

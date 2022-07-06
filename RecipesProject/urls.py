from django.contrib import admin
from django.urls import path
from RecipesApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('recipes/', Recipes.as_view(), name='recipes'),
    path('recipes/add/', AddRecipe.as_view(), name='add-recipe'),
    path('allergen/add/', AddAllergen.as_view(), name='add-allergen'),
]

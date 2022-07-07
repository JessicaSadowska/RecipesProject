from django.contrib import admin
from django.urls import path
from RecipesApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='main_page'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('recipes/', Recipes.as_view(), name='recipes'),
    path('recipes/<int:recipe_id>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('recipes/add/', AddRecipe.as_view(), name='add_recipe'),
    path('recipes/delete/<int:pk>/', DeleteRecipe.as_view(), name='delete_recipe'),
    path('recipes/update/<int:pk>/', UpdateRecipe.as_view(), name='update_recipe'),
    path('allergen/add/', AddAllergen.as_view(), name='add_allergen'),
]

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
    path('allergen/', Allergens.as_view(), name='allergens'),
    path('allergen/add/', AddAllergen.as_view(), name='add_allergen'),
    path('allergen/delete/<int:pk>/', DeleteAllergen.as_view(), name='delete_allergen'),
    path('category/', Categories.as_view(), name='categories'),
    path('category/add/', AddCategory.as_view(), name='add_category'),
    path('category/delete/<int:pk>/', DeleteCategory.as_view(), name='delete_category'),
    path('category/recipes/<int:pk>/', RecipesInCategory.as_view(), name='recipes_in_category'),
]

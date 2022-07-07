from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_list_or_404
from django.utils.decorators import method_decorator
from django.views import View, generic
from RecipesApp import forms
from django.contrib.auth.models import User
from .models import *


class MainPage(View):
    def get(self, request):
        return render(request, 'base.html')


class Register(View):
    def get(self, request):
        form = forms.RegisterForm()

        return render(
            request,
            'register.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email')
            )

            return redirect('login')

        else:
            return render(
                request,
                'register.html',
                context={
                    'form': form
                }
            )


class Login(View):
    def get(self, request):
        form = forms.LoginForm()

        return render(
            request,
            'login.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                msg = "Zalogowano"
            else:
                msg = "Niepoprawne dane logowania"

            return render(
                request,
                'login.html',
                context={
                    'msg': msg,
                    'form': form,
                }
            )

        else:
            return render(
                request,
                'login.html',
                context={
                    'form': form,
                }
            )


class Logout(View):
    def get(self, request):
        if request.user:
            logout(request)

        return redirect('login')


class Recipes(View):
    def get(self, request):
        recipes = get_list_or_404(Recipe)

        return render(
            request,
            'recipes_list.html',
            context={
                'recipes': recipes
            }
        )


class RecipeDetail(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)

        return render(
            request,
            'recipe_detail.html',
            context={
                'recipe': recipe
            }
        )


@method_decorator(login_required, name='dispatch')
class AddRecipe(generic.CreateView):
    model = Recipe
    fields = "__all__"
    success_url = '/recipes/'
    template_name = 'add_recipe.html'


@method_decorator(login_required, name='dispatch')
class DeleteRecipe(generic.DeleteView):
    model = Recipe
    success_url = '/recipes/'
    template_name = 'delete_recipe.html'


@method_decorator(login_required, name='dispatch')
class UpdateRecipe(generic.UpdateView):
    model = Recipe
    fields = "__all__"
    template_name = 'update_recipe.html'
    success_url = '/recipes/'

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class Allergens(View):
    def get(self, request):
        allergens = get_list_or_404(Allergen)

        return render(
            request,
            'allergen_list.html',
            context={
                'allergens': allergens
            }
        )


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddAllergen(generic.CreateView):
    model = Allergen
    fields = "__all__"
    success_url = '/allergen/'
    template_name = 'add_allergen.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class DeleteAllergen(generic.DeleteView):
    model = Allergen
    success_url = '/allergen/'
    template_name = 'delete_allergen.html'


class Categories(View):
    def get(self, request):
        categories = get_list_or_404(Category)

        return render(
            request,
            'category_list.html',
            context={
                'categories': categories
            }
        )


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddCategory(generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = '/category/'
    template_name = 'add_category.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class DeleteCategory(generic.DeleteView):
    model = Category
    success_url = '/category/'
    template_name = 'delete_category.html'


class RecipesInCategory(View):
    def get(self, request, category_id):

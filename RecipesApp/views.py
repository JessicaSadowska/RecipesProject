from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View, generic
from RecipesApp import forms
from .forms import AddRecipeForm, AddDietForm, AddOpinionForm
from .models import *


class MainPage(View):
    def get(self, request):
        """
        Return the base template rendered.
        :template: base.html
        """
        return render(request, 'base.html')


class Register(View):
    def get(self, request):
        """
        Return the register form.
        :template: register.html
        """
        form = forms.RegisterForm()

        return render(
            request,
            'register.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """
        Register new user if data is valid and redirect to login page.
        Render register form again if data is invalid.
        :template: register.html
        """
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
        """
        Return the login form.
        :template: login.html
        """
        form = forms.LoginForm()

        return render(
            request,
            'login.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        """
        Login user if data is valid.
        Render login form again if data is invalid.
        :template: login.html
        """
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                msg = "Zalogowano!"
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
        """
        Log user out and redirect to login page.
        """
        if request.user:
            logout(request)

        return redirect('login')


class Recipes(View):
    def get(self, request):
        """
        Display all instances of :model:`RecipesApp.Recipe`.
        :template:`recipes_list.html`
        """
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
        """
        Display an individual :model:`RecipesApp.Recipe` with a given id.
        :param recipe_id: integer
        :template:`recipe_detail.html`
        """
        recipe = Recipe.objects.get(id=recipe_id)
        allergens = recipe.allergens.all()
        opinions = recipe.opinion_set.all()

        return render(
            request,
            'recipe_detail.html',
            context={
                'recipe': recipe,
                'allergens': allergens,
                'opinions': opinions,
            }
        )


@method_decorator(login_required, name='dispatch')
class AddRecipe(generic.CreateView):
    """
    Creates a new instance of :model:`RecipesApp.Recipe` and redirects
    to recipes list view.
    :form_class: 'AddRecipeForm'
    :template:`add_recipe.html`
    """
    model = Recipe
    form_class = AddRecipeForm
    success_url = '/recipes/'
    template_name = 'add_recipe.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class DeleteRecipe(generic.DeleteView):
    """
    Deletes the instance of :model:`RecipesApp.Recipe` and redirects
    to recipes list view.
    :template:`delete_recipe.html`
    """
    model = Recipe
    success_url = '/recipes/'
    template_name = 'delete_recipe.html'


@method_decorator(login_required, name='dispatch')
class UpdateRecipe(generic.UpdateView):
    """
    Updates the instance of :model:`RecipesApp.Recipe` and redirects
    to recipes list view.
    :template:`update_recipe.html`
    """
    model = Recipe
    form_class = AddRecipeForm
    template_name = 'update_recipe.html'
    success_url = '/recipes/'


class Diets(View):
    def get(self, request):
        """
        Display all instances of :model:`RecipesApp.Diet`.
        :template:`diets_list.html`
        """
        diets = get_list_or_404(Diet)

        return render(
            request,
            'diets_list.html',
            context={
                'diets': diets
            }
        )


class DietDetail(View):
    def get(self, request, diet_id):
        """
        Display an individual :model:`RecipesApp.Diet` with a given id.
        :param diet_id: integer
        :template:`diet_detail.html`
        """
        diet = Diet.objects.get(id=diet_id)
        recipes = diet.meals.all()
        kcal = 0
        proteins = 0
        carbs = 0
        fats = 0

        for recipe in recipes:
            kcal += recipe.kcal
            proteins += recipe.proteins
            carbs += recipe.carbs
            fats += recipe.fats

        return render(
            request,
            'diet_detail.html',
            context={
                'diet': diet,
                'recipes': recipes,
                'kcal': kcal,
                'proteins': proteins,
                'carbs': carbs,
                'fats': fats,
            }
        )


@method_decorator(login_required, name='dispatch')
class AddDiet(generic.CreateView):
    """
    Creates a new instance of :model:`RecipesApp.Diet` and redirects
    to diet list view.
    :form_class: 'AddDietForm'
    :template:`add_diet.html`
    """
    model = Diet
    form_class = AddDietForm
    success_url = '/diets/'
    template_name = 'add_diet.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class DeleteDiet(generic.DeleteView):
    """
    Deletes the instance of :model:`RecipesApp.Diet` and redirects
    to diet list view.
    :template:`delete_diet.html`
    """
    model = Diet
    success_url = '/diets/'
    template_name = 'delete_diet.html'


@method_decorator(login_required, name='dispatch')
class UpdateDiet(generic.UpdateView):
    """
    Updates the instance of :model:`RecipesApp.Diet` and redirects
    to diet list view.
    :template:`update_diet.html`
    """
    model = Diet
    form_class = AddDietForm
    template_name = 'update_diet.html'
    success_url = '/diets/'


@method_decorator(login_required, name='dispatch')
class Allergens(View):
    def get(self, request):
        """
        Display all instances of :model:`RecipesApp.Allergen`.
        :template:`allergen_list.html`
        """
        allergens = get_list_or_404(Allergen)

        return render(
            request,
            'allergen_list.html',
            context={
                'allergens': allergens
            }
        )


@method_decorator(login_required, name='dispatch')
class AddAllergen(generic.CreateView):
    """
    Creates a new instance of :model:`RecipesApp.Allergen` and redirects
    to allergen list view.
    :template:`add_allergen.html`
    """
    model = Allergen
    fields = "__all__"
    success_url = '/allergen/'
    template_name = 'add_allergen.html'


@method_decorator(login_required, name='dispatch')
class DeleteAllergen(generic.DeleteView):
    """
    Deletes the instance of :model:`RecipesApp.Allergen` and redirects
    to allergen list view.
    :template:`delete_allergen.html`
    """
    model = Allergen
    success_url = '/allergen/'
    template_name = 'delete_allergen.html'


class Categories(View):
    def get(self, request):
        """
        Display all instances of :model:`RecipesApp.Category`.
        :template:`category_list.html`
        """
        categories = get_list_or_404(Category)

        return render(
            request,
            'category_list.html',
            context={
                'categories': categories
            }
        )


@method_decorator(login_required, name='dispatch')
class AddCategory(generic.CreateView):
    """
    Creates a new instance of :model:`RecipesApp.Category` and redirects
    to category list view.
    :template:`add_category.html`
    """
    model = Category
    fields = "__all__"
    success_url = '/category/'
    template_name = 'add_category.html'


@method_decorator(login_required, name='dispatch')
class DeleteCategory(generic.DeleteView):
    """
    Deletes the instance of :model:`RecipesApp.Category` and redirects
    to category list view.
    :template:`delete_category.html`
    """
    model = Category
    success_url = '/category/'
    template_name = 'delete_category.html'


class RecipesInCategory(View):
    def get(self, request, category_id):
        """
        Display all instances of :model:`RecipesApp.Recipe` in a given category.
        :param category_id: integer
        :template:`recipes_in_category_list.html`
        """
        category = Category.objects.get(id=category_id)
        recipes_in_category = get_list_or_404(Recipe.objects.filter(category=category))

        return render(
            request,
            'recipes_in_category_list.html',
            context={
                'recipes': recipes_in_category,
                'category': category,
            }
        )


@method_decorator(login_required, name='dispatch')
class MyRecipes(View):
    def get(self, request, user_id):
        """
        Display all instances of :model:`RecipesApp.Recipe` created by a given user.
        :param user_id: integer
        :template:`recipes_list.html`
        """
        user = User.objects.get(id=user_id)
        user_recipes = user.recipe_set.all()

        return render(
            request,
            'recipes_list.html',
            context={
                'recipes': user_recipes
            }
        )


@method_decorator(login_required, name='dispatch')
class MyDiets(View):
    def get(self, request, user_id):
        """
        Display all instances of :model:`RecipesApp.Diet` created by a given user.
        :param user_id: integer
        :template:`diets_list.html`
        """
        user = User.objects.get(id=user_id)
        user_diets = user.diet_set.all()

        return render(
            request,
            'diets_list.html',
            context={
                'diets': user_diets
            }
        )


@method_decorator(login_required, name='dispatch')
class AddOpinion(generic.CreateView):
    """
    Creates a new instance of :model:`RecipesApp.Opinion` and redirects
    to recipe detail view.
    :form_class:`AddOpinionForm`
    :template:`add_opinion.html`
    """
    model = Opinion
    form_class = AddOpinionForm
    template_name = 'add_opinion.html'

    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.recipe = self.recipe
        return super().form_valid(form)

    def get_success_url(self):
        recipe_id = self.kwargs["recipe_id"]
        return reverse("recipe_detail", kwargs={"recipe_id": recipe_id})


@method_decorator(login_required, name='dispatch')
class DeleteOpinion(generic.DeleteView):
    """
    Deletes the instance of :model:`RecipesApp.Opinion` and redirects
    to recipe detail view.
    :template:`delete_opinion.html`
    """
    model = Opinion
    template_name = 'delete_opinion.html'

    def get_success_url(self):
        opinion_id = self.kwargs["pk"]
        opinion = Opinion.objects.get(id=opinion_id)
        recipe_id = opinion.recipe.id
        return reverse("recipe_detail", kwargs={"recipe_id": recipe_id})


@method_decorator(login_required, name='dispatch')
class UpdateOpinion(generic.UpdateView):
    """
    Updates the instance of :model:`RecipesApp.Opinion` and redirects
    to recipe detail view.
    :template:`update_opinion.html`
    """
    model = Opinion
    form_class = AddOpinionForm
    template_name = 'update_opinion.html'

    def get_success_url(self):
        opinion_id = self.kwargs["pk"]
        opinion = Opinion.objects.get(id=opinion_id)
        recipe_id = opinion.recipe.id
        return reverse("recipe_detail", kwargs={"recipe_id": recipe_id})



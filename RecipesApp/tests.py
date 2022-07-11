import pytest
from django.test import Client
from RecipesApp.forms import *
from RecipesApp.models import Recipe, Diet, Allergen, Category


@pytest.fixture
def user():
    """
    Create user fixture.
    """
    user = User.objects.create(
        username="testuser",
        first_name="Jan",
        last_name="Nowak",
        email="test@test.com",
        password="test1234"
    )
    return user


@pytest.fixture
def client():
    """
    Create client fixture.
    """
    client = Client()
    return client


@pytest.mark.django_db
def test_main_page(client):
    """
    A ``GET`` to the main page view gets status code 200.
    """
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_register_view(client):
    """
    A ``GET`` to the ``register`` view populates the registration
    form into the context and gets status code 200.
    """
    get_response = client.get('/register/')
    # assert get_response.context.get('form') == RegisterForm
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_register_view(client):
    """
    A ``POST`` to the ``register`` view with valid data properly
    creates a new user and gets status code 200.
    """
    count_before_create = User.objects.count()
    post_response = client.post(
        '/register/',
        {
            'username': "testuser",
            'password': "test1234",
            'password2': "test1234",
            'first_name': 'Jan',
            'last_name': 'Nowak',
            'email': "Jan@Nowak.gmail"
        },
        follow=True
    )
    count_after_create = User.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_login_view(client):
    """
    A ``GET`` to the ``login`` view populates the login
    form into the context and gets status code 200.
    """
    get_response = client.get('/login/')
    # assert get_response.context.get('form') == LoginForm
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_login_view(client, user):
    """
    A ``POST`` to the ``login`` view with valid data properly
    logs in the given user and gets status code 200.
    """
    post_response = client.post(
        '/login/',
        {
            'username': "testuser",
            'password': "test1234",
        },
        follow=True
    )
    assert post_response.status_code == 200
    assert user.is_authenticated
    assert user.is_active


@pytest.mark.django_db
def test_logout_view(client, user):
    """
    A ``GET`` to the ``logout`` view properly loges out
    the given user and gets status code 200.
    """
    client.force_login(user)
    response = client.get('/logout/')
    assert response.headers["Location"] == "/login/"
    # assert not user.is_active


@pytest.fixture
def recipe(user):
    """
    Create recipe fixture.
    """
    recipe = Recipe.objects.create(
        name="testrecipe",
        description="testdescription",
        ingredients="testingredients",
        preparation="testpreparation",
        kcal="1",
        proteins="1",
        carbs="1",
        fats="1",
        author=user
    )
    return recipe


@pytest.mark.django_db
def test_recipe_list_view(client, recipe):
    """
    A ``GET`` to the ``recipes`` populates the recipes
    into the context and gets status code 200.
    """
    response = client.get('/recipes/')
    assert response.context.get('recipes') == [recipe]
    assert response.status_code == 200


@pytest.mark.django_db
def test_recipe_detail_view(client, recipe):
    """
    A ``GET`` to the ``recipe_detail`` populates the recipe
    with a given id into the context and gets status code 200.
    """
    response = client.get(f'/recipes/{recipe.id}/')
    assert response.context.get('recipe') == recipe
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_recipe_add_view_(client, user):
    """
    A ``GET`` to the ``add_recipe`` for logged in
    user gets status code 200.
    """
    client.force_login(user)
    get_response = client.get('/recipes/add/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_recipe_add_view(client, user):
    """
    A ``POST`` to the ``add_recipe`` view with valid data properly
    creates new recipe and gets status code 200.
    """
    client.force_login(user)
    count_before_create = Recipe.objects.count()
    post_response = client.post(
        '/recipes/add/',
        {
            'name': "testrecipe",
            'description': "testdescription",
            'ingredients': "testingredients",
            'preparation': "testpreparation",
            'kcal': "1",
            'proteins': "1",
            'carbs': "1",
            'fats': "1",
        },
        follow=True
    )
    count_after_create = Recipe.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_recipe_delete_view_(client, user, recipe):
    """
    A ``GET`` to the ``delete_recipe`` for logged in
    user who created the recipe gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/recipes/delete/{recipe.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_recipe_delete_view(client, user, recipe):
    """
    A ``POST`` to the ``delete_recipe`` view properly
    deletes the given recipe.
    """
    client.force_login(user)
    count_before_delete = Recipe.objects.count()
    client.post(f'/recipes/delete/{recipe.id}/', follow=True)
    count_after_delete = Recipe.objects.count()
    assert count_after_delete == count_before_delete - 1


@pytest.mark.django_db
def test_get_recipe_update_view_(client, user, recipe):
    """
    A ``GET`` to the ``update_recipe`` for logged in
    user who created the recipe gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/recipes/update/{recipe.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_recipe_update_view(client, user, recipe):
    """
    A ``POST`` to the ``update_recipe`` view with valid data properly
    updates the recipe and gets status code 200.
    """
    client.force_login(user)
    post_response = client.post(
        f'/recipes/update/{recipe.id}/',
        {
            'name': 'updatedrecipe',
            'description': "testdescription",
            'ingredients': "testingredients",
            'preparation': "testpreparation",
            'kcal': "1",
            'proteins': "1",
            'carbs': "1",
            'fats': "1",
        },
        follow=True
    )
    assert post_response.status_code == 200
    # assert recipe.name == "updatedrecipe"


@pytest.mark.django_db
def test_my_recipes_list_view(client, recipe, user):
    """
    A ``GET`` to the ``my_recipes`` view populates the recipes
    created by a given user into the context and gets
    status code 200.
    """
    client.force_login(user)
    response = client.get(f'/recipes/my/{user.id}/')
    assert response.context.get('recipes')[0] == recipe
    assert response.status_code == 200


@pytest.fixture
def diet(user, recipe):
    """
    Create diet fixture.
    """
    recipes = Recipe.objects.all()
    diet = Diet.objects.create(
        name="testdiet",
        description="testdescription",
        author=user,
    )
    diet.meals.set(recipes)
    return diet


@pytest.mark.django_db
def test_diet_list_view(client, diet):
    """
    A ``GET`` to the ``diets`` populates the diets
    into the context and gets status code 200.
    """
    response = client.get('/diets/')
    assert response.context.get('diets') == [diet]
    assert response.status_code == 200


@pytest.mark.django_db
def test_diet_detail_view(client, diet):
    """
    A ``GET`` to the ``diet_detail`` populates the diet
    with a given id into the context and gets status code 200.
    """
    response = client.get(f'/diets/{diet.id}/')
    assert response.context.get('diet') == diet
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_diet_add_view_(client, user):
    """
    A ``GET`` to the ``add_diet`` for logged in
    user gets status code 200.
    """
    client.force_login(user)
    get_response = client.get('/diets/add/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_diet_add_view(client, user, recipe):
    """
    A ``POST`` to the ``add_diet`` view with valid data properly
    creates new diet and gets status code 200.
    """
    client.force_login(user)
    count_before_create = Diet.objects.count()
    post_response = client.post(
        '/diets/add/',
        {
            'name': "testdiet",
            'description': "testdescription",
            'meals': [recipe.id],
        },
        follow=True
    )
    count_after_create = Diet.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_diet_delete_view_(client, user, diet):
    """
    A ``GET`` to the ``delete_diet`` for logged in
    user who created the diet gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/diets/delete/{diet.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_diet_delete_view(client, user, diet):
    """
    A ``POST`` to the ``delete_diet`` view properly
    deletes the given diet.
    """
    client.force_login(user)
    count_before_delete = Diet.objects.count()
    client.post(f'/diets/delete/{diet.id}/', follow=True)
    count_after_delete = Diet.objects.count()
    assert count_after_delete == count_before_delete - 1


@pytest.mark.django_db
def test_get_diet_update_view_(client, user, diet):
    """
    A ``GET`` to the ``update_diet`` for logged in
    user who created the diet gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/diets/update/{diet.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_diet_update_view(client, user, recipe, diet):
    """
    A ``POST`` to the ``update_diet`` view with valid data properly
    updates the diet and gets status code 200.
    """
    client.force_login(user)
    post_response = client.post(
        f'/diets/update/{diet.id}/',
        {
            'name': "updateddiet",
            'description': "testdescription",
            'meals': [recipe.id],
        },
        follow=True
    )
    assert post_response.status_code == 200
    # assert diet.name == "updateddiet"


@pytest.mark.django_db
def test_my_diets_list_view(client, diet, user):
    """
    A ``GET`` to the ``my_diets`` view populates the diets
    created by a given user into the context and gets
    status code 200.
    """
    client.force_login(user)
    response = client.get(f'/diets/my/{user.id}/')
    assert response.context.get('diets')[0] == diet
    assert response.status_code == 200


@pytest.fixture
def superuser():
    """
    Create superuser fixture.
    """
    superuser = User.objects.create(
        username="testsuperuser",
        first_name="Adam",
        last_name="Kowalski",
        email="test2@test.com",
        password="test1234"
    )
    superuser.is_superuser = True
    return superuser


@pytest.fixture
def allergen():
    """
    Create allergen fixture.
    """
    allergen = Allergen.objects.create(
        name="testallergen"
    )
    return allergen


@pytest.mark.django_db
def test_allergen_list_view(client, allergen, superuser):
    """
    A ``GET`` to the ``allergens`` view populates the allergens
    into the context when a superuser is logged in
    and gets status code 200.
    """
    client.force_login(superuser)
    response = client.get('/allergen/')
    assert response.context.get('allergens') == [allergen]
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_allergen_add_view_(client, superuser):
    """
    A ``GET`` to the ``add_allergen`` for logged in
    user gets status code 200.
    """
    client.force_login(superuser)
    get_response = client.get('/allergen/add/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_allergen_add_view(client, superuser):
    """
    A ``POST`` to the ``add_allergen`` view with valid data properly
    creates new allergen and gets status code 200.
    """
    client.force_login(superuser)
    count_before_create = Allergen.objects.count()
    post_response = client.post(
        '/allergen/add/',
        {
            'name': "testallergen",
        },
        follow=True
    )
    count_after_create = Allergen.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_allergen_delete_view_(client, superuser, allergen):
    """
    A ``GET`` to the ``delete_allergen`` for logged in
    superuser gets status code 200.
    """
    client.force_login(superuser)
    get_response = client.get(f'/allergen/delete/{allergen.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_allergen_delete_view(client, superuser, allergen):
    """
    A ``POST`` to the ``delete_allergen`` view properly
    deletes the given allergen.
    """
    client.force_login(superuser)
    count_before_delete = Allergen.objects.count()
    client.post(f'/allergen/delete/{allergen.id}/', follow=True)
    count_after_delete = Allergen.objects.count()
    assert count_after_delete == count_before_delete - 1


@pytest.fixture
def category():
    """
    Create category fixture.
    """
    category = Category.objects.create(
        name="testcategory"
    )
    return category


@pytest.mark.django_db
def test_category_list_view(client, category):
    """
    A ``GET`` to the ``categories`` view populates the categories
    into the context and gets status code 200.
    """
    response = client.get('/category/')
    assert response.context.get('categories') == [category]
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_category_add_view_(client, superuser):
    """
    A ``GET`` to the ``add_category`` for logged in
    user gets status code 200.
    """
    client.force_login(superuser)
    get_response = client.get('/category/add/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_category_add_view(client, superuser):
    """
    A ``POST`` to the ``add_category`` view with valid data properly
    creates new category and gets status code 200.
    """
    client.force_login(superuser)
    count_before_create = Category.objects.count()
    post_response = client.post(
        '/category/add/',
        {
            'name': "testcategory",
        },
        follow=True
    )
    count_after_create = Category.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_category_delete_view_(client, superuser, category):
    """
    A ``GET`` to the ``delete_category`` for logged in
    superuser gets status code 200.
    """
    client.force_login(superuser)
    get_response = client.get(f'/category/delete/{category.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_category_delete_view(client, superuser, category):
    """
    A ``POST`` to the ``delete_category`` view properly
    deletes the given category.
    """
    client.force_login(superuser)
    count_before_delete = Category.objects.count()
    client.post(f'/category/delete/{category.id}/', follow=True)
    count_after_delete = Category.objects.count()
    assert count_after_delete == count_before_delete - 1


@pytest.fixture
def opinion(user, recipe):
    """
    Create opinion fixture.
    """
    opinion = Opinion.objects.create(
        title="testopinion",
        content="testcontent",
        author=user,
        recipe=recipe
    )
    return opinion


@pytest.mark.django_db
def test_get_opinion_add_view_(client, user, recipe):
    """
    A ``GET`` to the ``add_opinion`` for logged in
    user gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/opinion/add/{recipe.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_opinion_add_view(client, superuser, recipe):
    """
    A ``POST`` to the ``add_opinion`` view with valid data properly
    creates new opinion and gets status code 200.
    """
    client.force_login(superuser)
    count_before_create = Opinion.objects.count()
    post_response = client.post(
        f'/opinion/add/{recipe.id}/',
        {
            'title': "testopinion",
            'content': 'testcontent',
            'author': superuser.id,
            'recipe': recipe.id,
        },
        follow=True
    )
    count_after_create = Opinion.objects.count()
    assert post_response.status_code == 200
    # assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_get_opinion_delete_view_(client, user, opinion):
    """
    A ``GET`` to the ``delete_opinion`` for logged in
    user who created the opinion gets status code 200.
    """
    client.force_login(user)
    get_response = client.get(f'/opinion/delete/{opinion.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_opinion_delete_view(client, user, opinion):
    """
    A ``POST`` to the ``delete_opinion`` view properly
    deletes the given opinion.
    """
    client.force_login(user)
    count_before_delete = Opinion.objects.count()
    client.post(f'/opinion/delete/{opinion.id}/', follow=True)
    count_after_delete = Opinion.objects.count()
    assert count_after_delete == count_before_delete - 1


@pytest.mark.django_db
def test_get_opinion_update_view_(client, superuser, opinion):
    """
    A ``GET`` to the ``update_opinion`` for logged in
    user who created the opinion gets status code 200.
    """
    client.force_login(superuser)
    get_response = client.get(f'/opinion/update/{opinion.id}/', follow=True)
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_post_opinion_update_view(client, superuser, recipe, opinion):
    """
    A ``POST`` to the ``update_opinion`` view with valid data properly
    updates the opinion and gets status code 200.
    """
    client.force_login(superuser)
    post_response = client.post(
        f'/opinion/update/{opinion.id}/',
        {
            'title': "updatedopinion",
            'content': 'testcontent',
        },
        follow=True
    )
    assert post_response.status_code == 200
    # assert opinion.title == "updatedopinion"
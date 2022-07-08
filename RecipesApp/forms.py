from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from RecipesApp.models import Diet, Recipe


class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')


class RegisterForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    first_name = forms.CharField(label='Imię')
    last_name = forms.CharField(label='Nazwisko')
    email = forms.EmailField(label='e-mail')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasła nie są identyczne")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError("Podany użytkownik już istnieje")
        return username


class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author', )
        widgets = {
            'allergens': forms.CheckboxSelectMultiple,
            'category': forms.CheckboxSelectMultiple,
        }
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'ingredients': 'Potrzebne składniki',
            'preparation': 'Sposób przygotowania',
            'kcal': 'Kalorie',
            'proteins': 'Białko',
            'carbs': 'Węglowodany',
            'fats': 'Tłuszcze',
            'allergens': 'Alergeny',
            'category': 'Kategorie',
            'image': 'Zdjęcie'

        }


class AddDietForm(forms.ModelForm):

    class Meta:
        model = Diet
        exclude = ('author', 'kcal')
        widgets = {
            'meals': forms.CheckboxSelectMultiple,
        }
        labels = {
            'name': 'Nazwa',
            'description': 'Opis',
            'meals': 'Lista posiłków',
        }


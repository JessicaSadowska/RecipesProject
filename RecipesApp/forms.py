from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

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

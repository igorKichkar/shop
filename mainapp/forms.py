from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User

DEFAULT_STYLE = {'attrs': {'class': 'form-control w-50'}}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(**DEFAULT_STYLE))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(**DEFAULT_STYLE))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(**DEFAULT_STYLE))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(**DEFAULT_STYLE))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(**DEFAULT_STYLE))
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(**DEFAULT_STYLE))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(**DEFAULT_STYLE))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(**DEFAULT_STYLE))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(**DEFAULT_STYLE))

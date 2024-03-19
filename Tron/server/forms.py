from django import forms

from .models import User


class RegistrationForm(forms.Form):
    user_flesh_id = forms.CharField(label='Индификатор пользователя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите IDF'}))
    username = forms.CharField(label='Придумайте логин', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}))
    password = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}))
    confirm_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
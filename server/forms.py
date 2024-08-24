from django import forms
from django.core.exceptions import ValidationError

from .models import UserCustom


class RegistrationForm(forms.Form):
    user_flesh_id = forms.CharField(label='Индификатор пользователя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите IDF'}))
    username = forms.CharField(label='Придумайте логин', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}))
    password = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}))
    confirm_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserCustom.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))


class ChatAuthenticationForm(forms.Form):
    token = forms.CharField(label='Аунтификация чата', max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Токен должен состоять из 20 символов',
               'autocomplete': 'off'}))
    first_key = forms.CharField(label='Первый ключ', max_length=1, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Любой символ, кроме цифры', 'autocomplete': 'off'}))
    second_key = forms.CharField(label='Второй ключ', max_length=3, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Любая цифра', 'autocomplete': 'off'}))
    image = forms.ImageField(label='Загрузить изображение', required=False)

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not token or len(token) != 20:
            raise ValidationError('Токен должен состоять из 20 символов')
        return token

    def clean_first_key(self):
        first_key = self.cleaned_data.get('first_key')
        if not first_key.isalpha():
            raise ValidationError('Первый ключ должен содержать только буквы')
        return first_key

    def clean_second_key(self):
        second_key = self.cleaned_data.get('second_key')
        if not second_key.isdigit():
            raise ValidationError('Второй ключ должен быть цифрой')
        return second_key


class SupportForm(forms.Form):
    name = forms.CharField( max_length=155, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Напишите ваше имя',
               'autocomplete': 'off'}))
    mail = forms.EmailField( max_length=155, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Напишите вашу почту', 'autocomplete': 'off'}))
    dsc = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Опишите вашу проблему', 'autocomplete': 'off'}))
    category = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': "hidden", 'value': 'Problems_with_site', 'placeholder': 'Ваша категория', 'autocomplete': 'off'}))


class CatSupportForm(forms.Form):
    category_site = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': "hidden", 'value': 'Problems_with_site',
               'placeholder': 'Ваша категория', 'autocomplete': 'off'}))
    category_idf = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': "hidden", 'value': 'Problems_with_IDF',
               'placeholder': 'Ваша категория', 'autocomplete': 'off'}))
    category_money = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': "hidden", 'value': 'Problems_with_money',
               'placeholder': 'Ваша категория', 'autocomplete': 'off'}))
    category_other = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': "hidden", 'value': 'Other',
               'placeholder': 'Ваша категория', 'autocomplete': 'off'}))

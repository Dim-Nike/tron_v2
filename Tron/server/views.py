from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


from .models import *

from .forms import RegistrationForm, LoginForm




def show_chat(req):

    data = {
        'title': 'Чаты'
    }

    return render(req, 'server/chat.html', data)


def show_login(req):
    form = LoginForm()
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('home')  # Перенаправление на главную страницу после успешного входа
            else:
                form.add_error('username', 'Неверные учетные данные')  # Добавляем ошибку, если вход не удался
    data = {
        'title': 'Авторизация',
        'form': form
    }

    return render(req, 'server/login.html', data)

def show_register(req):
    form = RegistrationForm()
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        fleshs = Flesh.objects.filter(is_active=True, is_use_user=False)
        user_flesh_id = form['user_flesh_id'].value()
        username = form['username'].value()
        password = form['password'].value()
        confirm_password = form['confirm_password'].value()
        user_flesh = next((flesh for flesh in fleshs if user_flesh_id == flesh.IDF), None)

        if user_flesh is not None:
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    form.add_error('username', 'Пользователь с таким логином уже существует')
                else:
                    user = User.objects.create_user(username=username, password=password, flesh=user_flesh)
                    user_flesh.is_use_user = True
                    user_flesh.save()
                    return redirect('login')
            else:
                form.add_error('confirm_password', 'Пароли не совпадают')
        else:
            form.add_error('user_flesh_id', 'Неверный IDF')

    data = {
        'title': 'Регистрация',
        'form': form
    }
    return render(req, 'server/register.html', data)

def show_index(req):
    data = {
        'title': 'Главная',
        'num_msg': '70',
        'num_dialog': '80',
    }

    return render(req, 'server/index-crypto.html', data)
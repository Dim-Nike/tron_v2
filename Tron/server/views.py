from django.shortcuts import render

def show_index(req):

    data = {
        'title': 'Чаты'
    }

    return render(req, 'server/chat.html', data)


def show_login(req):

    data = {
        'title': 'Авторизация'
    }

    return render(req, 'server/login.html', data)


def show_register(req):

    data = {
        'title': 'Регистрация'
    }
    return render(req, 'server/register.html', data)
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .models import *

from .forms import RegistrationForm, LoginForm


def pattern_view(req):
    data = {
        'user':  req.user
    }

    return render(req, 'server/technical/pattern.html', data)

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
                    user.balance_tariff = TariffBalances.objects.create(
                        count_msg_user=0,
                        count_change_key=user.flesh.tariff.count_change_key,
                        count_msg=user.flesh.tariff.count_msg,
                        count_dialog=user.flesh.tariff.count_dialog,
                        count_update_tariff=user.flesh.tariff.count_update_tariff
                    )
                    user.payments.add(Payment.objects.create(
                        category='purchase',
                        dsc=f'Приобретение новой флешки с тарифом "{user.flesh.tariff.name}"',
                        price=user.flesh.price
                    ))
                    user.save()
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

@login_required
def show_index(req):
    key_identification = req.user.identification_dialog
    if req.user.identification_dialog is not None:
        is_check_key_identification = True
    else:
        is_check_key_identification = False

    data_user = {
        'count_msg': [
            req.user.balance_tariff.count_msg,
            req.user.flesh.tariff.count_msg,
            req.user.balance_tariff.count_msg*1000 // req.user.flesh.tariff.count_msg*1000 // 10000

        ],
        'count_dialog': [
            req.user.balance_tariff.count_dialog,
            req.user.flesh.tariff.count_dialog,
            req.user.balance_tariff.count_dialog*1000 // req.user.flesh.tariff.count_dialog*1000 // 10000
        ],
        'count_change_key': [
            req.user.balance_tariff.count_change_key,
            req.user.flesh.tariff.count_change_key,
            req.user.balance_tariff.count_change_key*1000 // req.user.flesh.tariff.count_change_key*1000 // 10000
        ],
        'count_update_tariff': [
            req.user.balance_tariff.count_update_tariff,
            req.user.flesh.tariff.count_update_tariff,
            req.user.balance_tariff.count_update_tariff*1000 // req.user.flesh.tariff.count_update_tariff*1000 // 10000
        ],
        'delay': req.user.flesh.tariff.delay, 'mess_ln': req.user.flesh.tariff.mess_ln,
        'deg_protection': req.user.flesh.tariff.deg_protection,
        'count_msg_user': req.user.balance_tariff.count_msg_user,
        'is_check_key_identification': is_check_key_identification
    }
    print(is_check_key_identification)
    # is_check_key_identification =1


    data = {
        'title': 'Главная',
        'data_user': data_user

    }

    return render(req, 'server/index-crypto.html', data)


@login_required
def show_profile(req):
    payments = req.user.payments.all()

    data = {
        'user': req.user,
        'payments': payments
    }
    return render(req, 'server/author-profile.html', data)



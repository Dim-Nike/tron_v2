from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import secrets
import string
from chat.models import Room
from .models import *

from .forms import RegistrationForm, LoginForm, ChatAuthenticationForm


def pattern_view(req):
    pari_user = None
    if req.user.status_idf == 'not_connect' and req.user.identification_dialog is None or req.user.status_idf == '':
        pass
    else:
        pari_user = req.user.identification_dialog.user_connect.exclude(id=req.user.id).first()

    data = {
        'user': req.user,
        'pari_user': pari_user
    }

    return render(req, 'server/technical/pattern.html', data)


def show_chat(req):
    data = {
        'title': 'Чаты'
    }

    return render(req, 'server/../chat/templates/chat.html', data)


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
                if UserCustom.objects.filter(username=username).exists():
                    form.add_error('username', 'Пользователь с таким логином уже существует')
                else:
                    user = UserCustom.objects.create_user(username=username, password=password, flesh=user_flesh)
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
            req.user.balance_tariff.count_msg * 1000 // req.user.flesh.tariff.count_msg * 1000 // 10000

        ],
        'count_dialog': [
            req.user.balance_tariff.count_dialog,
            req.user.flesh.tariff.count_dialog,
            req.user.balance_tariff.count_dialog * 1000 // req.user.flesh.tariff.count_dialog * 1000 // 10000
        ],
        'count_change_key': [
            req.user.balance_tariff.count_change_key,
            req.user.flesh.tariff.count_change_key,
            req.user.balance_tariff.count_change_key * 1000 // req.user.flesh.tariff.count_change_key * 1000 // 10000
        ],
        'count_update_tariff': [
            req.user.balance_tariff.count_update_tariff,
            req.user.flesh.tariff.count_update_tariff,
            req.user.balance_tariff.count_update_tariff * 1000 // req.user.flesh.tariff.count_update_tariff * 1000 // 10000
        ],
        'delay': req.user.flesh.tariff.delay, 'mess_ln': req.user.flesh.tariff.mess_ln,
        'deg_protection': req.user.flesh.tariff.deg_protection,
        'count_msg_user': req.user.balance_tariff.count_msg_user,
        'is_check_key_identification': is_check_key_identification,
        'status_idf': req.user.status_idf
    }

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


def show_form_idf(req):
    status_info_user = ['start', 'connection_successful', 'connection_error', 'add_new_obj', 'add_error',
                        'start_chat_error', 'update']
    print(req.user.identification_dialog)

    if req.user.identification_dialog is not None:
        info_user = status_info_user[-1]
    else:
        info_user = status_info_user[0]

    if req.method == 'POST':
        form = ChatAuthenticationForm(req.POST, req.FILES)

        if form.is_valid():
            auth_dialog = form.cleaned_data['token']
            first_key = form.cleaned_data['first_key']
            second_key = form.cleaned_data['second_key']

            # Проверка на попытку подключения к самому себе
            if req.user.identification_dialog and ObjIdfDialog.objects.filter(
                    user_connect=req.user, idf_dialog__token_dialog=auth_dialog).exists():
                info_user = status_info_user[5]  # Устанавливаем информацию о пользователе как ошибка
            else:
                if ObjIdfDialog.objects.filter(is_use=False, idf_dialog__token_dialog=auth_dialog).exists():
                    obj_idf_dialog = ObjIdfDialog.objects.get(is_use=False, idf_dialog__token_dialog=auth_dialog)
                    idf_dialog = obj_idf_dialog.idf_dialog.first()
                    if first_key == idf_dialog.f_key and second_key == idf_dialog.s_key and idf_dialog.is_active == True:
                        if req.user.identification_dialog is not None:
                            key_idf_to_delete = req.user.identification_dialog.idf_dialog.first()
                            req.user.identification_dialog.user_connect.remove(req.user)
                            req.user.identification_dialog.idf_dialog.remove(key_idf_to_delete)
                            if req.user.identification_dialog.user_connect.count() > 0:
                                pair_user = req.user.identification_dialog.user_connect.first()
                                if pair_user:
                                    pair_user.status_idf = 'waiting'
                                    pair_user.save()
                            req.user.identification_dialog.is_use = False
                            req.user.identification_dialog.status = 'waiting'
                            req.user.identification_dialog.save()
                            req.user.status_idf = 'not_connect'
                            req.user.save()
                        new_key_idf_user = KeyIdentification.objects.create(
                            token_dialog=auth_dialog,
                            f_key=first_key,
                            s_key=second_key,
                            image_key=req.FILES['image'],
                            is_active=True
                        )
                        obj_idf_dialog.idf_dialog.add(new_key_idf_user)
                        obj_idf_dialog.user_connect.add(req.user)
                        obj_idf_dialog.status = 'connected'
                        req.user.identification_dialog = obj_idf_dialog
                        obj_idf_dialog.is_use = True
                        req.user.status_idf = 'connected'
                        req.user.save()
                        obj_idf_dialog.save()
                        pair_user = req.user.identification_dialog.user_connect.exclude(id=req.user.id).first()
                        if pair_user:
                            pair_user.status_idf = 'connected'
                            pair_user.save()
                        info_user = status_info_user[1]
                    else:
                        info_user = status_info_user[2]

                else:
                    if ObjIdfDialog.objects.filter(is_use=True, idf_dialog__token_dialog=auth_dialog).exists():
                        info_user = status_info_user[4]
                    else:
                        if req.user.identification_dialog is not None:
                            key_idf_to_delete = req.user.identification_dialog.idf_dialog.first()
                            req.user.identification_dialog.user_connect.remove(req.user)
                            req.user.identification_dialog.idf_dialog.remove(key_idf_to_delete)
                            if req.user.identification_dialog.user_connect.count() > 0:
                                pair_user = req.user.identification_dialog.user_connect.exclude(
                                    id=req.user.id).first()
                                if pair_user:
                                    pair_user.status_idf = 'waiting'
                                    pair_user.save()
                            req.user.identification_dialog.is_use = False
                            req.user.identification_dialog.status = 'waiting'
                            req.user.identification_dialog.save()
                            req.user.status_idf = 'not_connect'
                            req.user.save()

                        idf_dialog = KeyIdentification.objects.create(
                            token_dialog=auth_dialog,
                            f_key=first_key,
                            s_key=second_key,
                            image_key=req.FILES['image'],
                            is_active=True
                        )
# ----------------------------------------------------------------------------------------------------------
                        new_obj_idf_dialog = ObjIdfDialog.objects.create(
                            status='waiting',
                            is_use=False,
                        )
                        new_obj_idf_dialog.idf_dialog.add(idf_dialog)
                        new_obj_idf_dialog.user_connect.add(req.user)
                        new_obj_idf_dialog.save()
                        req.user.identification_dialog = new_obj_idf_dialog
                        req.user.status_idf = 'waiting'
                        req.user.save()
                        info_user = status_info_user[3]
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            info_user = ', '.join(error_messages)
    else:
        form = ChatAuthenticationForm()

    print(info_user)

    data = {
        'form': form,
        'info_user': info_user
    }

    return render(req, 'server/form-layout.html', data)

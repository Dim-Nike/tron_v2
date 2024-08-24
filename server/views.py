from datetime import datetime
import random

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
import base64
from django.core.files.base import ContentFile

import secrets
import string
# from chat.models import Room
from .models import *

from .forms import RegistrationForm, LoginForm, ChatAuthenticationForm, SupportForm, CatSupportForm
from .scripts import *

from .scripts.encrypt import ESRS, noise_list, en_msg, ERSR_number
from .scripts.decoding import ESRS, noise_list, de_msg


def pattern_view(req):
    pari_user = None
    if req.user.status_idf == 'not_connect' and req.user.identification_dialog is None or req.user.status_idf == '':
        pass
    else:
        pari_user = req.user.identification_dialog.user_connect.exclude(id=req.user.id).first()

    cat_news = CatNews.objects.all()

    data = {
        'user': req.user,
        'pari_user': pari_user,
        'catNews': cat_news
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

    def generate_ref_token(length=15):
        symbols = string.ascii_letters + string.digits
        reference_code = ''.join(random.choice(symbols) for _ in range(length))
        # Проверка уникальности кода платежа
        while UserCustom.objects.filter(rif_token=reference_code).exists():
            reference_code = ''.join(random.choice(symbols) for _ in range(length))
        return reference_code

    reference_code = req.GET.get('ref')
    if reference_code is not None:
        user_custom = UserCustom.objects.filter(rif_token=reference_code).first()
        if user_custom is not None:
            if req.user is not None:
                if req.user == user_custom:
                    reference_user = 'Error self'
                else:
                    reference_user = user_custom
            else:
                reference_user = user_custom
        else:
            reference_user = 'Error code'
    else:
        reference_user = 'Not code'
    if req.method == 'POST':
        if reference_user != 'Not code':
            if reference_user.balance_tariff.count_invited_user <= 0:
                reference_user = 'Error_limit_invate_user'
            else:
                form = RegistrationForm(req.POST)
                fleshes = Flesh.objects.filter(is_active=True, is_use_user=False)
                user_flesh_id = form['user_flesh_id'].value()
                username = form['username'].value()
                password = form['password'].value()
                confirm_password = form['confirm_password'].value()
                user_flesh = next((flesh for flesh in fleshes if user_flesh_id == flesh.IDF), None)
                if user_flesh is not None:
                    if password == confirm_password:
                        if UserCustom.objects.filter(username=username).exists():
                            form.add_error('username', 'Пользователь с таким логином уже существует')
                        else:
                            user = UserCustom.objects.create_user(username=username, password=password,
                                                                  flesh=user_flesh, rif_token=generate_ref_token())
                            user_flesh.is_use_user = True
                            user_flesh.save()
                            user.balance_tariff = TariffBalances.objects.create(
                                count_msg_user=0,
                                count_invited_user=user.flesh.tariff.count_invited_user,
                                count_msg=user.flesh.tariff.count_msg,
                                count_dialog=user.flesh.tariff.count_dialog,
                                count_withdrawal=user.flesh.tariff.count_withdrawal,
                            )
                            user.payments.add(Payment.objects.create(
                                category='purchase',
                                dsc=f'Приобретение новой флешки с тарифом "{user.flesh.tariff.name}"',
                                tech_msg='Отсутствует',
                                status='successful',
                                price=user.flesh.price
                            ))

                            if reference_user == 'Not code' or reference_user == 'Error self' or reference_user == 'Error code':
                                pass
                            else:
                                user.payments.add(Payment.objects.create(
                                    category='enrollment',
                                    dsc=f'Зачисление бонусов за использовании реферальной программой',
                                    tech_msg='Отсутствует',
                                    status='successful',
                                    percent_price=user.flesh.tariff.financial_constraints.reward_ref,
                                    price=int(
                                        user.flesh.price * user.flesh.tariff.financial_constraints.reward_ref / 100)
                                ))
                                user.reference_user = reference_user
                                user.internal_cash_account += int(
                                        user.flesh.price * user.flesh.tariff.financial_constraints.reward_ref / 100)

                                reference_user.payments.add(Payment.objects.create(
                                    category='enrollment',
                                    dsc=f'Вашей реферальной ссылкой воспользовался {user}',
                                    tech_msg='Отсутствует',
                                    status='successful',
                                    percent_price=reference_user.flesh.tariff.financial_constraints.reward_ref,
                                    price=int(
                                        user.flesh.price * reference_user.flesh.tariff.financial_constraints.reward_ref / 100)
                                ))
                                reference_user.internal_cash_account += int(
                                    user.flesh.price * reference_user.flesh.tariff.financial_constraints.reward_ref / 100)
                                reference_user.balance_tariff.count_invited_user -= 1
                                reference_user.balance_tariff.save()
                                user.save()
                                reference_user.save()
                            user.save()
                            return redirect('login')
                    else:
                        form.add_error('confirm_password', 'Пароли не совпадают')
                else:
                    form.add_error('user_flesh_id', 'Неверный IDF')
        else:
            form = RegistrationForm(req.POST)
            fleshes = Flesh.objects.filter(is_active=True, is_use_user=False)
            user_flesh_id = form['user_flesh_id'].value()
            username = form['username'].value()
            password = form['password'].value()
            confirm_password = form['confirm_password'].value()
            user_flesh = next((flesh for flesh in fleshes if user_flesh_id == flesh.IDF), None)
            if user_flesh is not None:
                if password == confirm_password:
                    if UserCustom.objects.filter(username=username).exists():
                        form.add_error('username', 'Пользователь с таким логином уже существует')
                    else:
                        user = UserCustom.objects.create_user(username=username, password=password, flesh=user_flesh,
                                                              rif_token=generate_ref_token())
                        user_flesh.is_use_user = True
                        user_flesh.save()
                        user.balance_tariff = TariffBalances.objects.create(
                            count_msg_user=0,
                            count_invited_user=user.flesh.tariff.count_invited_user,
                            count_msg=user.flesh.tariff.count_msg,
                            count_dialog=user.flesh.tariff.count_dialog,
                            count_withdrawal=user.flesh.tariff.count_withdrawal,
                        )
                        user.payments.add(Payment.objects.create(
                            category='purchase',
                            dsc=f'Приобретение новой флешки с тарифом "{user.flesh.tariff.name}"',
                            tech_msg='Отсутствует',
                            status='successful',
                            price=user.flesh.price
                        ))

                        if reference_user == 'Not code' or reference_user == 'Error self' or reference_user == 'Error code':
                            pass
                        else:
                            user.payments.add(Payment.objects.create(
                                category='enrollment',
                                dsc=f'Зачисление бонусов за использовании реферальной программой',
                                tech_msg='Отсутствует',
                                status='successful',
                                price=int(user.flesh.price / 10)
                            ))
                            user.reference_user = reference_user
                            user.internal_cash_account += int(user.flesh.price / 10)
                            reference_user.payments.add(Payment.objects.create(
                                category='enrollment',
                                dsc=f'Вашей реферальной ссылкой воспользовался {user}',
                                tech_msg='Отсутствует',
                                status='successful',
                                price=int(
                                    user.flesh.price * reference_user.flesh.tariff.financial_constraints.reward_ref / 100)
                            ))
                            reference_user.internal_cash_account += int(
                                user.flesh.price * reference_user.flesh.tariff.financial_constraints.reward_ref / 100)
                            reference_user.balance_tariff.count_invited_user -= 1
                            reference_user.balance_tariff.save()
                            user.save()
                            reference_user.save()
                        user.save()
                        return redirect('login')
                else:
                    form.add_error('confirm_password', 'Пароли не совпадают')
            else:
                form.add_error('user_flesh_id', 'Неверный IDF')
    data = {
        'title': 'Регистрация',
        'form': form,
        'reference_user': reference_user
    }
    return render(req, 'server/register.html', data)


def show_tariffs(req):
    licenses = []

    licenses_dsc = [
        ['1', 'Что-то', 'Что-то', 'Что-то', 'Что-то', ],
        ['2', 'Что-то', 'Что-то', 'Что-то', 'Что-то', ],
        ['3', 'Что-то', 'Что-то', 'Что-то', 'Что-то', ],
    ]

    licenses_patch_img = [
        'server/assets/images/icons/pricing-one-1.png',
        'server/assets/images/icons/pricing-one-2.png',
        'server/assets/images/icons/pricing-one-3.png',
    ]

    licenses_price = [
        [Tariff.objects.filter(name_license='base').order_by('price').all()[0].price,
         Tariff.objects.filter(name_license='base').order_by('price').last().price,
         ],
        [
            Tariff.objects.filter(name_license='professionale').order_by('price').all()[0].price,
            Tariff.objects.filter(name_license='professionale').order_by('price').last().price,
        ],
        [
            Tariff.objects.filter(name_license='premium').order_by('price').all()[0].price,
            Tariff.objects.filter(name_license='premium').order_by('price').last().price,
        ]
    ]

    for i, el in enumerate(Tariff.LICENSES_FIELD):
        licenses.append([el[1]])
        licenses[i].append(licenses_dsc[i])
        licenses[i].append(licenses_patch_img[i])
        licenses[i].append(licenses_price[i])
        licenses[i].append(el[0])

    data = {
        'licenses': licenses
    }
    return render(req, 'server/tariffs.html', data)


def show_tariff_user(req):
    user = req.user

    def generate_payment_code(length=20):
        symbols = string.ascii_letters + string.digits
        payment_code = ''.join(random.choice(symbols) for _ in range(length))
        # Проверка уникальности кода платежа
        while Payment.objects.filter(technical_comment=payment_code).exists():
            payment_code = ''.join(random.choice(symbols) for _ in range(length))
        return payment_code

    user.technical_comment = generate_payment_code(length=20)
    user.save()
    tariffs = Tariff.objects.filter(id=req.user.flesh.tariff.id).all()
    data = {
        'user': user,
        'tariff': tariffs
    }
    return render(req, 'server/tariff_user.html', data)


def show_detail_tariff(req):
    tariffs = req.GET.get('license', 'base')
    print(f'Watch GET {tariffs}')
    data = {
        'tariff': Tariff.objects.filter(name_license=tariffs).order_by('price').all()
    }
    return render(req, 'server/detail_tariff.html', data)


def show_tariff_buy(req, pk):
    user = req.user

    def generate_payment_code(length=20):
        symbols = string.ascii_letters + string.digits
        payment_code = ''.join(random.choice(symbols) for _ in range(length))
        # Проверка уникальности кода платежа
        while Payment.objects.filter(technical_comment=payment_code).exists():
            payment_code = ''.join(random.choice(symbols) for _ in range(length))
        return payment_code

    user.technical_comment = generate_payment_code(length=20)
    user.save()
    tariffs = Tariff.objects.filter(id=pk).all()
    if tariffs[0].category_market == 'unavailable' or tariffs[0].category_market == 'in processing':
        status_tariff_buy = 'unavailable'
    elif tariffs[0] == req.user.flesh.tariff:
        status_tariff_buy = 'update'
    else:
        status_tariff_buy = 'on sale'
    data = {
        'user': user,
        'tariff': tariffs,
        'status_tariff_buy': status_tariff_buy
    }
    return render(req, 'server/tariff_buy.html', data)


def payments_tariff(req, pk):
    user = req.user
    tariff = Tariff.objects.filter(id=pk).all()
    user.payments.add(Payment.objects.create(
        category='purchase',
        dsc=f'Приобретение тарифа {tariff[0].name}',
        price=tariff[0].price,
        status='waiting',
        technical_comment=user.technical_comment,
        tariff=tariff[0]
    ))
    user.save()
    return redirect('home')


def update_tariff(req, pk):
    user = req.user
    tariff = Tariff.objects.filter(id=pk).all()
    user.payments.add(Payment.objects.create(
        category='update',
        dsc=f'Обновление тарифа {tariff[0].name}',
        price=tariff[0].price_update,
        status='waiting',
        technical_comment=user.technical_comment,
        tariff=tariff[0]
    ))
    user.save()
    return redirect('home')


def update_tariff_internal_cash_account(req, pk):
    tariff = Tariff.objects.filter(id=pk).all()
    if req.user.internal_cash_account > tariff[0].price_update:
        req.user.payments.add(Payment.objects.create(
            category='purchase_bonuses',
            dsc=f'Обновление тарифа {tariff[0].name} через внутренний счет',
            price=tariff[0].price_update,
            status='successful',
            technical_comment='Отсутствует',
            tariff=tariff[0]
        ))

        req.user.flesh.tariff = tariff[0]
        req.user.balance_tariff = TariffBalances.objects.create(
            count_msg_user=0,
            count_invited_user=tariff[0].count_invited_user,
            count_msg=tariff[0].count_msg,
            count_dialog=tariff[0].count_dialog,
            count_withdrawal=tariff[0].count_withdrawal
        )
        req.user.internal_cash_account -= tariff[0].price_update
        req.user.flesh.save()
        req.user.balance_tariff.save()
        req.user.save()
        if req.user.reference_user is not None:
            req.user.reference_user.payments.add(Payment.objects.create(
                category='enrollment',
                dsc=f'{req.user} обновил тариф через внутренний счет',
                percent_price=req.user.reference_user.flesh.tariff.financial_constraints.reward_ref,
                price=tariff[0].price_update * req.user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100,
                status='successful',
                technical_comment='Отсутствует',
            ))
            req.user.reference_user.internal_cash_account += req.user.flesh.price * req.user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100
            req.user.reference_user.save()
        return redirect('home')
    else:
        req.user.payments.add(Payment.objects.create(
            category='purchase_bonuses',
            dsc=f'Не хватает денежных средств на внутреннем счете на тариф {tariff[0].name}',
            price=tariff[0].price_update,
            status='rejected',
            technical_comment='Отсутствует',
            tariff=tariff[0]
        ))
        req.user.save()
        return redirect('home')


def payments_tariff_internal_cash_account(req, pk):
    tariff = Tariff.objects.filter(id=pk).all()
    if req.user.internal_cash_account > tariff[0].price_update:
        req.user.payments.add(Payment.objects.create(
            category='purchase_bonuses',
            dsc=f'Приобретение тарифа {tariff[0].name} через внутренний счет',
            price=tariff[0].price,
            status='successful',
            technical_comment='Отсутствует',
            tariff=tariff[0]
        ))

        req.user.flesh.tariff = tariff[0]
        req.user.balance_tariff = TariffBalances.objects.create(
            count_msg_user=0,
            count_invited_user=tariff[0].count_invited_user,
            count_msg=tariff[0].count_msg,
            count_dialog=tariff[0].count_dialog,
            count_withdrawal=tariff[0].count_withdrawal
        )
        req.user.internal_cash_account -= tariff[0].price
        req.user.flesh.save()
        req.user.balance_tariff.save()
        req.user.save()

        if req.user.reference_user is not None:
            req.user.reference_user.payments.add(Payment.objects.create(
                category='enrollment',
                dsc=f'{req.user} купил тариф {tariff[0].name} через внутренний счет',
                percent_price=req.user.reference_user.flesh.tariff.financial_constraints.reward_ref,
                price=tariff[0].price * req.user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100,
                status='successful',
                technical_comment='Отсутствует',
            ))
            req.user.reference_user.internal_cash_account += req.user.flesh.price * req.user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100
            req.user.reference_user.save()

        return redirect('home')
    else:
        req.user.payments.add(Payment.objects.create(
            category='purchase_bonuses',
            dsc=f'Не хватает денежных средств на внутреннем счете на тариф {tariff[0].name}',
            price=tariff[0].price,
            status='rejected',
            technical_comment='Отсутствует',
            tariff=tariff[0]
        ))
        req.user.save()
        return redirect('home')


def adding_funds(req):
    if req.method == 'POST':
        replenishment = req.POST.get('replenishment')
        print(replenishment)
    return redirect('home')


def show_report_category(req):
    payment_category_l = {
        'purchase': [0, 0, 0, '', '', ''],
        'update': [0, 0, 0, '', '', ''],
        'purchase_bonuses': [0, 0, 0, '', '', ''],
        'enrollment': [0, 0, 0, '', '', '', []],
        'withdrawal': [0, 0, [], '', '', '', [], 0],
        'replenishment': [0, 0, [], '', '', '', [], 0],
    }
    total_price = 0
    for el in req.user.payments.all():
        if el.category in payment_category_l:
            payment_category_l[el.category][1] += 1
            if el.status == 'successful':
                if el.category == 'replenishment' or el.category == 'withdrawal':
                    payment_category_l[el.category][2].append(el.price_start)
                    payment_category_l[el.category][6].append(el.percent_price)
                else:
                    payment_category_l[el.category][2] += el.price
                if el.category == 'replenishment' or el.category == 'withdrawal':
                    total_price += el.price_start
                else:
                    total_price += el.price

            if el.category == 'purchase':
                payment_category_l[el.category][4] = 'Внешняя оплата'
                payment_category_l[el.category][5] = el.category
            elif el.category == 'update':
                payment_category_l[el.category][4] = 'Продление тарифа'
                payment_category_l[el.category][5] = el.category
            elif el.category == 'purchase_bonuses':
                payment_category_l[el.category][4] = 'Внутренняя оплата'
                payment_category_l[el.category][5] = el.category

            elif el.category == 'enrollment':
                payment_category_l[el.category][4] = 'Зачисления'
                payment_category_l[el.category][5] = el.category

            elif el.category == 'withdrawal':
                payment_category_l[el.category][4] = 'Вывод средств'
                payment_category_l[el.category][5] = el.category

            elif el.category == 'replenishment':
                payment_category_l[el.category][4] = 'Оплата на внутренний счет'
                payment_category_l[el.category][5] = el.category

    for el in payment_category_l:
        if el == 'replenishment' or el == 'withdrawal':
            payment_category_l[el][0] += round(sum(payment_category_l[el][2]) * 100 / total_price, 2)
        else:
            payment_category_l[el][0] += round(payment_category_l[el][2] * 100 / total_price, 2)
        if el == 'enrollment':
            payment_category_l[el][3] = round(
                req.user.flesh.tariff.financial_constraints.percentage_withdrawal * payment_category_l[el][2] / 100,
                2)
            if payment_category_l[el][2] != 0:
                payment_category_l[el][6] = round(payment_category_l[el][3] * 100 / payment_category_l[el][2], 2)
            else:
                payment_category_l[el][6] = 0
        elif el == 'replenishment' or el == 'withdrawal':
            if payment_category_l[el][6] != 0:
                sum_lost_profit = 0
                for i, _ in enumerate(payment_category_l[el][2]):
                    sum_lost_profit += round(payment_category_l[el][6][i] * payment_category_l[el][2][i] / 100, 2)
                payment_category_l[el][3] = sum_lost_profit
            else:
                payment_category_l[el][3] = 0

            if payment_category_l[el][3] != 0 or sum(payment_category_l[el][2]) != 0:
                payment_category_l[el][7] = round(payment_category_l[el][3] * 100 / sum(payment_category_l[el][2]), 2)
            else:
                payment_category_l[el][7] = 0
        else:
            payment_category_l[el][3] = 'Отсутствует'

    data = {
        'payment_category': payment_category_l,
        'withdrawal_sum': sum(payment_category_l['withdrawal'][2]),
        'replenishment_sum': sum(payment_category_l['replenishment'][2])
    }
    return render(req, 'server/report_category.html', data)


def show_detail_report(req):
    report = req.GET.get('license', 'enrollment')
    payments = req.user.payments.filter(category=report).order_by('date').all()
    # if report == 'withdrawal' or report == 'replenishment':
    #     percentage = req.user.flesh.tariff.financial_constraints.percentage_withdrawal
    # elif report == 'replenishment':
    #     for el in req.user.payments.filter(category='replenishment'):
    #         pass
    #     percentage = req.user.flesh.tariff.financial_constraints.percentage_admission
    # elif report == 'purchase' or report == 'update' or report == 'purchase_bonuses':
    #     percentage = 0
    # else:
    #     percentage = req.user.flesh.tariff.financial_constraints.percentage_withdrawal
    #
    # for el in payments:
    #     if el.status == 'successful':
    #          total_price += el.price
    #
    # lost_profits = round(percentage * total_price / 100, 2)
    # fact_price = total_price - lost_profits
    #
    # data = {
    #     'payments': payments,
    #     'total_price': total_price,
    #     'lost_profits': lost_profits,
    #     'fact_price': fact_price,
    #     'percentage': percentage,
    #     'last_date': payments.last().date,
    #     'category': payments[0].get_category_display
    # }
    value_payments = {
        'total_price': 0,
        'fact_price': 0,
        'lost_profit': 0,
        'percentage': 0,
        'el_lost_profit': [],
        'is_lost_profit': False,
    }
    if report == 'replenishment' or report == 'withdrawal':
        for el in payments:
            value_payments['total_price'] += el.price_start
            value_payments['el_lost_profit'].append(0)
            value_payments['lost_profit'] += el.price_start * el.percent_price / 100
            value_payments['fact_price'] += el.price_start - (el.price_start * el.percent_price / 100)
            value_payments['is_lost_profit'] = True
        value_payments['percentage'] = round(value_payments['lost_profit'] * 100 / value_payments['total_price'], 2)

    elif report == 'enrollment':
        for el in payments:
            value_payments['total_price'] += el.price
            value_payments['lost_profit'] += el.price * req.user.flesh.tariff.financial_constraints.percentage_withdrawal / 100
        value_payments['percentage'] = req.user.flesh.tariff.financial_constraints.percentage_withdrawal
        value_payments['fact_price'] = value_payments['total_price'] - value_payments['lost_profit']
        value_payments['is_lost_profit'] = True
    else:
        for el in payments:
            value_payments['total_price'] += el.price

    data = {
        'value_payments': value_payments,
        'payments': payments,
        'percent': req.user.flesh.tariff.financial_constraints.percentage_withdrawal,
        'report': report,
    }
    return render(req, 'server/detail_report.html', data)


def show_admin_tariff(req):
    if req.method == 'POST':
        input_text = req.POST.get('input_text')
        select_option = req.POST.get('select_option')
        payment = Payment.objects.get(technical_comment=input_text)
        payment.status = req.POST.get('select_option')
        payment.save()
        if select_option == 'successful':
            user = UserCustom.objects.get(payments__id=payment.id)
            if payment.category == 'withdrawal':
                print(
                    f'Payment - {int(payment.price + (int(payment.price) * user.flesh.tariff.financial_constraints.percentage_withdrawal / 100) + ((int(payment.price) * user.flesh.tariff.financial_constraints.percentage_withdrawal / 100) / user.flesh.tariff.financial_constraints.percentage_withdrawal))}')
                payment.dsc = 'Успешный вывод средств! Номер карты не доступен'
                user.internal_cash_account -= int(payment.price + (
                            int(payment.price) * user.flesh.tariff.financial_constraints.percentage_withdrawal / 100) + (
                                                              (
                                                                          int(payment.price) * user.flesh.tariff.financial_constraints.percentage_withdrawal / 100) / user.flesh.tariff.financial_constraints.percentage_withdrawal))
                user.balance_tariff.count_withdrawal -= payment.price
                payment.save()
                user.balance_tariff.save()
                user.save()
            elif payment.category == 'replenishment':
                user.internal_cash_account += payment.price
                user.save()
            else:
                user = UserCustom.objects.get(payments__id=payment.id)
                user.flesh.tariff = payment.tariff
                user.balance_tariff = TariffBalances.objects.create(
                    count_msg_user=0,
                    count_invited_user=payment.tariff.count_invited_user,
                    count_msg=payment.tariff.count_msg,
                    count_dialog=payment.tariff.count_dialog,
                    count_withdrawal=payment.tariff.count_withdrawal
                )
                user.flesh.save()
                user.balance_tariff.save()
                user.save()

                if user.reference_user is not None:
                    user.reference_user.payments.add(Payment.objects.create(
                        category='enrollment',
                        dsc=f'{user} приобрел/обновил тариф',
                        percent_price=user.reference_user.flesh.tariff.financial_constraints.reward_ref,
                        price=payment.price * user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100,
                        status='successful',
                        technical_comment='Отсутствует',
                    ))
                    user.reference_user.internal_cash_account += user.flesh.price * user.reference_user.flesh.tariff.financial_constraints.reward_ref / 100
                    user.reference_user.save()

    payments = Payment.objects.all()
    data = {
        'payments': payments,

    }
    return render(req, 'server/admin_tariff.html', data)


def show_payment_history(req):
    def generate_payment_code(length=20):
        symbols = string.ascii_letters + string.digits
        payment_code = ''.join(random.choice(symbols) for _ in range(length))
        # Проверка уникальности кода платежа
        while Payment.objects.filter(technical_comment=payment_code).exists():
            payment_code = ''.join(random.choice(symbols) for _ in range(length))
        return payment_code

    payments_technical_comment_l = []
    for el in req.user.payments.all():
        payments_technical_comment_l.append(el.technical_comment)
    if req.user.technical_comment in payments_technical_comment_l:
        req.user.technical_comment = generate_payment_code()
        req.user.save()

    if req.method == 'POST':
        if req.POST.get('replenishment') is None:
            bank_card = req.POST.get('bank_card')
            withdrawal_amount = req.POST.get('withdrawal_amount')
            msg = req.POST.get('msg')
            new_payment = Payment.objects.create(
                category='withdrawal',
                dsc=f'{bank_card} {msg}',
                price_start=withdrawal_amount,
                percent_price=req.user.flesh.tariff.financial_constraints.percentage_withdrawal,
                price=int(int(withdrawal_amount) - (
                            int(withdrawal_amount) * req.user.flesh.tariff.financial_constraints.percentage_withdrawal / 100)),
                status='waiting',
                technical_comment=req.user.technical_comment
            )
            if req.user.internal_cash_account < int(withdrawal_amount):
                new_payment.status = 'rejected'
                new_payment.msg = 'Не хватает денежных средств'
                new_payment.save()
            elif req.user.balance_tariff.count_withdrawal < int(withdrawal_amount):
                new_payment.status = 'unsuccessful'
                new_payment.msg = 'Сумма вывода превышает лимита вывода денежных средств'
                new_payment.save()

            req.user.payments.add(new_payment)
            req.user.save()
            return redirect('payment_history')
        else:
            replenishment = req.POST.get('replenishment')
            new_payment = Payment.objects.create(
                category='replenishment',
                dsc=f'Пополнение внутреннего баланса',
                price_start=replenishment,
                percent_price=req.user.flesh.tariff.financial_constraints.percentage_admission,
                price=int(int(replenishment) - (
                            int(replenishment) * req.user.flesh.tariff.financial_constraints.percentage_admission / 100)),
                status='waiting',
                technical_comment=req.user.technical_comment
            )
            req.user.payments.add(new_payment)
            req.user.save()
            return redirect('payment_history')
    data = {
        'payments': req.user.payments.all(),
        'technical_comment': req.user.technical_comment
    }

    return render(req, 'server/payment_history.html', data)


def show_referral_program(req):
    user_ref = UserCustom.objects.filter(reference_user=req.user).all()
    list_user_ref = [

    ]
    for el in user_ref:
        purchase_sum = 0
        update_sum = 0
        bonuses_sum = 0

        # TODO необходимо разобраться с реф токеном
        for payment in el.payments.filter(category='purchase').all():
            if payment.status == 'successful':
                purchase_sum += int(payment.price * payment.percent_price / 100)
                print(f'purchase - {payment.percent_price}')

        for payment in el.payments.filter(category='update').all():
            if payment.status == 'successful':
                update_sum += int(payment.price * payment.percent_price / 100)
                print(f'update - {payment.percent_price}')

        for payment in el.payments.filter(category='purchase_bonuses').all():
            if payment.status == 'successful':
                bonuses_sum += int(payment.price * payment.percent_price / 100)
                print(f'purchase_bonuses - {payment.percent_price}')

        list_user_ref.append(
            {'username': el.username,
             'tariff': el.flesh.tariff.name,
             'last_active': el.payments.order_by('-date').first(),
             'payments': purchase_sum + update_sum + bonuses_sum}
        )

    data = {
        'user_ref': list_user_ref
    }
    return render(req, 'server/referral_program.html', data)


@login_required(login_url='login')
def show_index(req):
    is_active_chat = req.user.status_connection
    news = News.objects.order_by('-date').all()
    last_news = news[:4] if len(news) >= 4 else news


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
        'count_invited_user': [
            req.user.balance_tariff.count_invited_user,
            req.user.flesh.tariff.count_invited_user,
            req.user.balance_tariff.count_invited_user * 1000 // req.user.flesh.tariff.count_invited_user * 1000 // 10000
        ],
        'count_withdrawal': [
            req.user.balance_tariff.count_withdrawal,
            req.user.flesh.tariff.count_withdrawal,
            req.user.balance_tariff.count_withdrawal * 1000 // req.user.flesh.tariff.count_withdrawal * 1000 // 10000
        ],
        'delay': req.user.flesh.tariff.delay,
        'mess_ln': req.user.flesh.tariff.mess_ln,
        'deg_protection': req.user.flesh.tariff.deg_protection,
        'count_msg_user': req.user.balance_tariff.count_msg_user,
        'is_check_key_identification': is_check_key_identification,
        'status_idf': req.user.status_idf
    }

    data = {
        'title': 'Главная',
        'is_active_chat': is_active_chat,
        'data_user': data_user,
        'news': last_news,

    }

    return render(req, 'server/index-crypto.html', data)


@login_required(login_url='login')
def show_profile(req):
    payments = req.user.payments.order_by('-date').all()
    last_three_payments = payments[:3] if len(payments) >= 3 else payments
    form = SupportForm(req.POST)
    cat_form = CatSupportForm(req.POST)

    if req.method == 'POST':
        form = SupportForm(req.POST)
        cat_form = CatSupportForm(req.POST)
        print(req.POST)
        name = req.POST['name']
        mail = req.POST['mail']
        dsc = req.POST['dsc']
        if 'category_site' in req.POST:
            category = req.POST['category_site']
        elif 'category_idf' in req.POST:
            category = req.POST['category_idf']
        elif 'category_money' in req.POST:
            category = req.POST['category_money']
        else:
            category = req.POST['category_other']
        new_support = Support.objects.create(
            category=category,
            name=name,
            mail=mail,
            dsc=dsc
        )
        new_support.save()
    else:
        form = SupportForm()




    data = {
        'user': req.user,
        'payments': last_three_payments,
        'form': form,
        'catForm': cat_form
    }
    return render(req, 'server/author-profile.html', data)


@login_required(login_url='login')
def show_form_idf(req):
    status_info_user = ['start', 'connection_successful', 'connection_error', 'add_new_obj', 'add_error',
                        'start_chat_error', 'update', 'await', 'error_user_count_dialog', 'error_pair_count_dialog']
    if not req.user.flesh.auth_chat:
        info_user = status_info_user[7]
    elif req.user.identification_dialog is not None:
        info_user = status_info_user[6]
    else:
        info_user = status_info_user[0]
    if req.method == 'POST':
        form = ChatAuthenticationForm(req.POST, req.FILES)
        if form.is_valid():
            auth_dialog = form.cleaned_data['token']
            first_key = form.cleaned_data['first_key']
            second_key = form.cleaned_data['second_key']
            img_patch = form.cleaned_data['image']
            img_patch = req.FILES['image']
            img_key_req = base64.b64encode(req.FILES['image'].read()).decode('utf-8')

            print(img_patch)

            # Проверка на авторизации флешки
            if req.user.flesh.auth_chat:
                # Проверка на попытку подключения к самому себе
                if req.user.identification_dialog and ObjIdfDialog.objects.filter(
                        user_connect=req.user, idf_dialog__token_dialog=auth_dialog).exists():
                    info_user = status_info_user[5]  # Устанавливаем информацию о пользователе как ошибка
                else:
                    if ObjIdfDialog.objects.filter(is_use=False, idf_dialog__token_dialog=auth_dialog).exists():
                        obj_idf_dialog = ObjIdfDialog.objects.get(is_use=False, idf_dialog__token_dialog=auth_dialog)
                        idf_dialog = obj_idf_dialog.idf_dialog.first()
                        with open(idf_dialog.image_key.path, 'rb') as img_file:
                            img_key = base64.b64encode(img_file.read()).decode('utf-8')
                        if first_key == idf_dialog.f_key and second_key == idf_dialog.s_key and img_key == img_key_req \
                                and idf_dialog.is_active:
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
                            pair_user = req.user.identification_dialog.user_connect.exclude(id=req.user.id).first()
                            if not req.user.balance_tariff.interlocutors.filter(id=pair_user.id).exists():
                                if req.user.balance_tariff.count_dialog <= 0:
                                    obj_idf_dialog.idf_dialog.remove(new_key_idf_user)
                                    obj_idf_dialog.user_connect.remove(req.user)
                                    obj_idf_dialog.status = 'waiting'
                                    req.user.identification_dialog = None
                                    req.user.save()
                                    obj_idf_dialog.save()
                                    info_user = status_info_user[8]
                                    data = {
                                        'form': form,
                                        'info_user': info_user
                                    }
                                    return render(req, 'server/form-layout.html', data)
                                else:
                                    req.user.balance_tariff.interlocutors.add(pair_user)
                                    req.user.balance_tariff.count_dialog -= 1
                                    req.user.balance_tariff.save()
                            if not pair_user.balance_tariff.interlocutors.filter(id=req.user.id).exists():
                                if pair_user.balance_tariff.count_dialog <= 0:
                                    obj_idf_dialog.idf_dialog.remove(new_key_idf_user)
                                    obj_idf_dialog.user_connect.remove(req.user)
                                    obj_idf_dialog.status = 'waiting'
                                    req.user.identification_dialog = None
                                    req.user.save()
                                    obj_idf_dialog.save()
                                    info_user = status_info_user[9]
                                    data = {
                                        'form': form,
                                        'info_user': info_user
                                    }
                                    return render(req, 'server/form-layout.html', data)

                                else:
                                    pair_user.balance_tariff.interlocutors.add(req.user)
                                    pair_user.balance_tariff.count_dialog -= 1
                                    pair_user.balance_tariff.save()
                            obj_idf_dialog.is_use = True
                            req.user.status_idf = 'connected'
                            req.user.flesh.is_save_key = False
                            req.user.flesh.save()
                            req.user.save()
                            obj_idf_dialog.save()
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
                            try:
                                msg_en = en_msg(msg_user='Проверка работоспсобности программы', ESRS=ESRS,
                                                f_key=first_key,
                                                img_path=r'C:\Users\User\Desktop\ИП Хорошко М.png',
                                                esrs_number=ERSR_number,
                                                s_key=second_key, noise_list=noise_list)

                                check_msg = de_msg(en_msg=msg_en, f_key=first_key, s_key=second_key, noise_l=noise_list,
                                                   img_path=r'C:\Users\User\Desktop\ИП Хорошко М.png', esrs=ESRS)
                                if check_msg == 'Проверка работоспсобности программы':
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
                                    req.user.flesh.is_save_key = False
                                    req.user.flesh.save()
                                    req.user.save()

                                    info_user = status_info_user[3]
                                else:
                                    info_user = 'key_warn'
                            except:
                                info_user = 'key_error'
            else:
                info_user = status_info_user[7]
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            info_user = ', '.join(error_messages)
    else:
        form = ChatAuthenticationForm()

    data = {
        'form': form,
        'info_user': info_user
    }

    return render(req, 'server/form-layout.html', data)


def show_cat_news(req):
    category_news = CatNews.objects.all()
    news = News.objects.all()
    list_news = {}
    for cat in category_news:
        list_news[cat.title] = []
        item = 0
        for i, new in enumerate(news):
            if cat.title == new.category.title:
                list_news[cat.title].append([])
                list_news[cat.title][item].append(item)
                list_news[cat.title][item].append(new.image.url)
                list_news[cat.title][item].append(new.title)
                list_news[cat.title][item].append(new.subtitle)
                list_news[cat.title][item].append(new.id)
                item += 1

    print(list_news)
    data = {
        'category_news': category_news,
        'news': news,
        'list_news': list_news
    }

    return render(req, 'server/cat_news.html', data)

def show_news(req, pk):
    news = News.objects.filter(category__id=pk).all()

    data = {
        'news': news
    }

    return render(req, 'server/news.html', data)


def show_detail_news(req, pk):
    news = News.objects.filter(id=pk).all()

    data = {
        'news': news
    }

    return render(req, 'server/detail_news.html', data)

@csrf_exempt
def auth_flesh(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        idf = Flesh.objects.filter(IDF=data['idf']).values()
        if 'code' in data and data['code'] == '1234':
            if not idf:
                return JsonResponse({'message': 'IDF не найден!'}, status=404)
            elif not idf[0]['is_use_user']:
                return JsonResponse({'message': 'IDF не зарегистрирован в системе. '
                                                'Пожалуйста, пройдите регистрацию на сайте и повторите операцию!'}
                                    , status=401)
            elif idf[0]['auth_chat']:
                return JsonResponse({'message': 'IDF уже авторизован! Операция не выполнена!'}, status=405)
            else:
                flesh = Flesh.objects.get(IDF=idf[0]['IDF'])
                flesh.auth_chat = True
                flesh.save()
                return JsonResponse(
                    {'message': 'Успешно!', 'idf_user': {'idf': flesh.IDF, 'auth_chat': flesh.auth_chat}}, status=200)
        else:
            return JsonResponse({'message': 'Ошибка подключения!'}, status=406)
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


@csrf_exempt
def online_connection_idf(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        idf = Flesh.objects.filter(IDF=data['idf']).values()
        if 'code' in data and data['code'] == '1234':
            if not idf:
                return JsonResponse({'message': 'IDF не найден!'}, status=404)
            else:
                flesh = Flesh.objects.get(IDF=idf[0]['IDF'])
                if flesh.auth_chat:
                    user = UserCustom.objects.get(flesh=flesh)
                    if user.flesh.is_save_key:
                        if user.status_idf == 'connected':
                            if user.status_connection is None:
                                new_obj_connect = ConnectIDF.objects.create(
                                    flesh_user=flesh,
                                    is_connect=True
                                )
                                user.status_connection = new_obj_connect
                                user.status_connection.save()
                                user.save()
                                return JsonResponse(
                                    {'message': 'Онлайн подключение создано!',
                                     'sleep_idf': user.status_connection.flesh_user.tariff.delay},
                                    status=201)
                            else:
                                print(data['key_idf'])
                                return JsonResponse({
                                    'message': 'Беспрерывное подключение!',
                                    'sleep_idf': user.status_connection.flesh_user.tariff.delay
                                }, status=200)

                        else:
                            return JsonResponse({
                                'message': 'Невозможно создать подключение! Дождитесь вашего собеседника!',
                            }, status=407)
                    else:
                        return JsonResponse(
                            {'message': 'Невозможно создать подключение! Ключи для шифрования отсутствуют'
                                        ' на локальном носителе!',
                             'ifd_user': user.flesh.is_save_key},
                            status=405
                        )
                else:
                    return JsonResponse(
                        {'message': 'Ошибка. Флешка не авторизована!'},
                        status=403)
        else:
            return JsonResponse({'message': 'Ошибка подключения!'}, status=406)
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


@csrf_exempt
def write_idf_key(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        idf = Flesh.objects.filter(IDF=data['idf']).values()
        if 'code' in data and data['code'] == '1234':
            if not idf:
                return JsonResponse({'message': 'IDF не найден!'}, status=404)
            else:
                flesh = Flesh.objects.get(IDF=idf[0]['IDF'])
                if flesh.auth_chat:
                    user = UserCustom.objects.get(flesh=flesh)
                    idf_identification = user.identification_dialog
                    if idf_identification:
                        key_identification = idf_identification.idf_dialog.all().first()
                        user.flesh.is_save_key = True
                        user.flesh.save()
                        user.save()

                        with open(key_identification.image_key.path, 'rb') as img_file:
                            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

                        return JsonResponse(
                            {'message': 'Создание ключей!',
                             'idf_user': {'token_dialog': key_identification.token_dialog,
                                          'f_key': key_identification.f_key,
                                          's_key': key_identification.s_key,
                                          'img_patch': encoded_string,
                                          'save_local': user.flesh.is_save_key
                                          }},
                            status=201)
                    else:
                        return JsonResponse(
                            {'message': 'Чат сервер не авторизован пользователем!'},
                            status=405
                        )
                else:
                    return JsonResponse(
                        {'message': 'Ошибка. Флешка не авторизована!'},
                        status=403)
        else:
            return JsonResponse({'message': 'Ошибка подключения!'}, status=406)
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


@csrf_exempt
def del_idf_connect(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        idf = Flesh.objects.filter(IDF=data['idf']).values()
        if 'code' in data and data['code'] == '1234':
            if not idf:
                return JsonResponse({'message': 'IDF не найден!'}, status=404)
            else:
                flesh = Flesh.objects.get(IDF=idf[0]['IDF'])
                if flesh.auth_chat:
                    user = UserCustom.objects.get(flesh=flesh)
                    if user.status_idf == 'waiting':
                        dialog = user.identification_dialog
                        user.identification_dialog = None
                        user.save()
                        user.status_idf = 'not_connect'
                        user.flesh.is_save_key = False
                        user.flesh.save()
                        user.save()
                        dialog.delete()
                        return JsonResponse({'message': 'Подключение разорвано! Ваш статус "Не подключен"'},
                                            status=203)
                    elif user.status_idf == 'connected':
                        dialog = user.identification_dialog

                        idf_d = ObjIdfDialog.objects.get(user_connect=user)
                        user_interlocutor = idf_d.user_connect.filter().exclude(username=user.username).first()

                        user.identification_dialog = None
                        user.status_connection = None
                        user.flesh.is_save_key = False
                        user.flesh.save()
                        user.status_idf = 'not_connect'
                        user.save()

                        user_interlocutor.identification_dialog = None
                        user_interlocutor.status_connection = None
                        user_interlocutor.flesh.is_save_key = False
                        user_interlocutor.flesh.save()
                        user_interlocutor.status_idf = 'not_connect'
                        user_interlocutor.save()

                        dialog.delete()
                        return JsonResponse({
                            'message': f'Соединение разорвано у вас и вашего собеседника {user_interlocutor}! Ваш статус "Не подключен"'},
                            status=203)

                    elif user.status_idf == 'not_connect':
                        return JsonResponse({'message': f'Ошибка операции, вы не подключены не к одному чат серверу'},
                                            status=409)
                else:
                    return JsonResponse(
                        {'message': 'Чат сервер не авторизован пользователем!'},
                        status=405
                    )
        else:
            return JsonResponse({'message': 'Ошибка подключения!'}, status=406)
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)

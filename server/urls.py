from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', show_index, name='home'),
    path('login', show_login, name='login'),
    path('register', show_register, name='register'),
    path('chat', show_chat, name='chat'),
    path('profile', show_profile, name='profile'),
    path('tariffs', show_tariffs, name='tariffs'),
    path('detail_tariff', show_detail_tariff, name='detail_tariff'),
    path('tariff_user', show_tariff_user, name='tariff_user'),
    path('update_tariff/<int:pk>', update_tariff, name='update_tariff'),
    path('update_tariff_internal_cash_account/<int:pk>', update_tariff_internal_cash_account,
         name='update_tariff_internal_cash_account'),
    path('detail_report', show_detail_report, name='detail_report'),
    path('tariff_buy/<int:pk>', show_tariff_buy, name='tariff_buy'),
    path('payments_tariff/<int:pk>', payments_tariff, name='payments_tariff'),
    path('payments_tariff_internal_cash_account/<int:pk>', payments_tariff_internal_cash_account,
         name='payments_tariff_internal_cash_account'),
    path('report_category', show_report_category, name='report_category'),
    path('admin_tariff', show_admin_tariff, name='admin_tariff'),
    path('payment_history', show_payment_history, name='payment_history'),
    path('adding_funds', adding_funds, name='adding_funds'),
    path('referral_program', show_referral_program, name='referral_program'),
    path('set-idf-form', show_form_idf, name='set-idf-form'),
    path('cat_news', show_cat_news, name='cat_news'),
    path('news/<int:pk>', show_news, name='news'),
    path('detail_news/<int:pk>', show_detail_news, name='detail_news'),
    path('auth_flesh', auth_flesh, name='auth_flesh'),
    path('write_key_idf', write_idf_key, name='write_key_idf'),
    path('del_idf_connect', del_idf_connect, name='del_idf_connect'),
    path('online_connection_idf', online_connection_idf, name='online_connection_idf')
    #todo создать доп анонимный чат для передачи ключей


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
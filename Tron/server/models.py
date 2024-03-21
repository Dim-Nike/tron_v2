from django.contrib.auth.models import AbstractUser
from django.db import models


class Tariff(models.Model):
    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    MARKET_FIELD = [
        ("on sale", "В продаже"),
        ('popular', 'Популярный'),
        ("unavailable", "Недоступен"),
        ("in processing", "В обработке"),
        ("new", "Новинка"),
        ("beneficial", "Выгодный"),

    ]

    LICENSES_FIELD = [
        ("base", "Базовый"),
        ('professionale', 'Проффисиональный'),
        ("premium", "Преимум"),
    ]


    category_market = models.CharField(verbose_name='Маркетинговое положение', choices=MARKET_FIELD, max_length=30)
    name = models.CharField(verbose_name='Название лицензии', default='none', max_length=20)
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    count_dialog = models.IntegerField(verbose_name='Количество диалогов', default=1)
    count_change_key = models.IntegerField(verbose_name='Количество смены ключа')
    count_update_tariff = models.IntegerField(verbose_name='Количество обновления тарифа')
    mess_ln = models.IntegerField(verbose_name='Длина сообщения')
    delay = models.IntegerField(verbose_name='Задержка', default=5)
    deg_protection = models.IntegerField(verbose_name='Степень защиты')
    name_license = models.CharField(verbose_name='Лицензия', choices=LICENSES_FIELD, max_length=20, default=LICENSES_FIELD[0])
    price = models.IntegerField(verbose_name='Стоимость', default=0, null=True, blank=True)
    price_update = models.IntegerField(verbose_name='Стоимость продления', default=0,)
    coupon = models.CharField(verbose_name='Купон(только на преимум)', max_length=20)

    def __str__(self):
        return  self.name




class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    flesh = models.ForeignKey('Flesh', verbose_name='ID флешки', on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_active_flesh = models.BooleanField(verbose_name='Активность аккаунта', default=True)
    rif_token = models.CharField(verbose_name='Реферальный токен', max_length=20, null=True, blank=True)
    photo = models.ImageField(verbose_name='Фотография', upload_to='user/photo/%Y/%m/%d/', null=True, blank=True)
    payments = models.ManyToManyField('Payment',  verbose_name='Платежные операции', null=True, blank=True)
    balance_tariff = models.ForeignKey('TariffBalances', verbose_name='Остаток тарифа', on_delete=models.PROTECT, null=True, blank=True)
    identification_dialog = models.ForeignKey('KeyIdentification', verbose_name='Индификация диалога', blank=True, null=True, on_delete=models.PROTECT)





class Flesh(models.Model):
    class Meta:
        verbose_name = 'Флешка'
        verbose_name_plural = 'Флешки'

    IDF = models.CharField(verbose_name='ИДФ', max_length=500)
    is_active = models.BooleanField(verbose_name='Активно', default=False)
    tariff = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.PROTECT)
    is_use_user = models.BooleanField(verbose_name='Используется?', default=False)
    count_flesh = models.IntegerField(verbose_name='Остаток флешек', default=0)
    price = models.IntegerField(verbose_name='Стоимость', default=0)


    def __str__(self):
        return self.IDF


class TariffBalances(models.Model):
    class Meta:
        verbose_name = 'Баланс тарифа'
        verbose_name_plural = 'Балансы тарифов'

    count_msg_user = models.IntegerField(verbose_name='Количество отправленных сообщений', default=0)
    count_change_key = models.IntegerField(verbose_name='Количество смены ключа', default=0)
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    count_dialog = models.IntegerField(verbose_name='Количество диалогов', default=1)
    count_update_tariff = models.IntegerField(verbose_name='Количество обновления тарифа')
    data_start = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    data_update = models.DateField(verbose_name='Дата обновления', auto_now=True)


class Payment(models.Model):
    class Meta:
        verbose_name = 'Платежная операция'
        verbose_name_plural = 'Платежные операции'

    CAT_FIELD = [
        ('purchase', 'Покупка'),
        ('update', 'Обновление'),
        ('purchase_bonuses', 'Оплата бонусами')
    ]
    category = models.CharField(verbose_name='Категория операции', max_length=30, choices=CAT_FIELD)
    dsc = models.CharField(verbose_name='Комментарий', max_length=55)
    price = models.IntegerField(verbose_name='Стоимость', default=0)
    date = models.DateTimeField(verbose_name='Дата операции', auto_now_add=True)


class KeyIdentification(models.Model):
    class Meta:
        verbose_name = 'Индификация ключа'
        verbose_name_plural = 'Индификация ключей'

    token_dialog = models.CharField(verbose_name='Токен авторизации диалога', max_length=100)
    s_key = models.CharField(verbose_name='Первый ключ(любой символ)', max_length=1)
    f_key = models.CharField(verbose_name='Первый ключ(любой символ)', max_length=1)
    image_key = models.ImageField(verbose_name='Картинка', upload_to='user/key/img_key/%Y/%m/%d/', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Актуальный')
    date_update = models.DateTimeField(verbose_name='Последнее обновление', auto_now_add=True)

    def __str__(self):
        return self.token_dialog




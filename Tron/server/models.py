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
    price = models.DecimalField(verbose_name='Стоимость', default=0, decimal_places=2, max_digits=5, null=True, blank=True)
    price_update = models.DecimalField(verbose_name='Стоимость продления', default=0, decimal_places=2, max_digits=5)
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
    balance_tariff = models.ForeignKey('TariffBalances', verbose_name='Остаток тарифа', on_delete=models.PROTECT, null=True, blank=True)





class Flesh(models.Model):
    class Meta:
        verbose_name = 'Флешка'
        verbose_name_plural = 'Флешки'

    IDF = models.CharField(verbose_name='ИДФ', max_length=500)
    is_active = models.BooleanField(verbose_name='Активно', default=False)
    tariff = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.PROTECT)
    is_use_user = models.BooleanField(verbose_name='Используется?', default=False)
    count_flesh = models.IntegerField(verbose_name='Остаток флешек', default=0)
    price = models.DecimalField(verbose_name='Стоимость', default=0, decimal_places=2, max_digits=3)


    def __str__(self):
        return self.IDF


class TariffBalances(models.Model):
    class Meta:
        verbose_name = 'Баланс тарифа'
        verbose_name_plural = 'Балансы тарифов'

    count_change_key = models.IntegerField(verbose_name='Количество смены ключа')
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    count_dialog = models.IntegerField(verbose_name='Количество диалогов', default=1)
    count_update_tariff = models.IntegerField(verbose_name='Количество обновления тарифа')
    data_start = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    data_update = models.DateField(verbose_name='Дата обновления', auto_now=True)

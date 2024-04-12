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


class UserCustom(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    STATUS_IDF_FIELDS = [
        ('not_connect', 'Не подключен'),
        ('waiting', 'В ожидании'),
        ('connected', 'Подключен')
    ]

    flesh = models.ForeignKey('Flesh', verbose_name='ID флешки', on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_active_flesh = models.BooleanField(verbose_name='Активность аккаунта', default=True)
    rif_token = models.CharField(verbose_name='Реферальный токен', max_length=20, null=True, blank=True)
    photo = models.ImageField(verbose_name='Фотография', upload_to='user/photo/%Y/%m/%d/', null=True, blank=True)
    payments = models.ManyToManyField('Payment',  verbose_name='Платежные операции', null=True, blank=True)
    balance_tariff = models.ForeignKey('TariffBalances', verbose_name='Остаток тарифа', on_delete=models.PROTECT, null=True, blank=True)
    status_idf = models.CharField(verbose_name='Статус подключения', choices=STATUS_IDF_FIELDS, max_length=20, default='not_connect')
    identification_dialog = models.ForeignKey('ObjIdfDialog', verbose_name='Объект индификации диалога',  blank=True, null=True, on_delete=models.PROTECT)



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
#
#
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

#
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

    token_dialog = models.CharField(verbose_name='Токен авторизации диалога', max_length=20)
    f_key = models.CharField(verbose_name='Первый ключ(любой смивол)', max_length=1)
    s_key = models.CharField(verbose_name='Второй ключ(любая цифра)', max_length=3)
    image_key = models.ImageField(verbose_name='Картинка', upload_to='user/key/img_key/%Y/%m/%d/', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Актуальный')
    date_update = models.DateTimeField(verbose_name='Последнее обновление', auto_now_add=True)

    def __str__(self):
        return self.token_dialog


class News(models.Model):
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    CAT_FIELD = [
        ('new', 'Новинка'),
        ('product', 'О продукте'),
        ('support', 'О сервисе'),
        ('tariff', 'О тарифах')
    ]

    title = models.CharField(verbose_name='Заголовок', max_length=155)
    category = models.CharField(verbose_name='Категория', choices=CAT_FIELD, max_length=20)
    dsc = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)


class ObjIdfDialog(models.Model):
    class Meta:
        verbose_name = 'Объект IDF диалога'
        verbose_name_plural = 'Объекты IDF диалога'

    STATUS_FIELD = [
        ('waiting', 'В ожидании'),
        ('connected', 'Подключено'),
    ]

    status = models.CharField(verbose_name='Статус', choices=STATUS_FIELD, max_length=10)
    idf_dialog = models.ManyToManyField(KeyIdentification, verbose_name='Индификаторы пользователей',)
    is_use = models.BooleanField(verbose_name='Используется', default=False)
    user_connect = models.ManyToManyField(to=UserCustom, verbose_name='Пользователи', default=None, null=True, blank=True)


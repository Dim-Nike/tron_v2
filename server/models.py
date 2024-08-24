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
        ("in processing", "В разработке"),
        ("new", "Новинка"),
        ("beneficial", "Выгодный"),

    ]

    LICENSES_FIELD = [
        ("base", "Базовый"),
        ('professionale', 'Для организаций'),
        ("premium", "Партнерам"),
    ]

    category_market = models.CharField(verbose_name='Маркетинговое положение', choices=MARKET_FIELD, max_length=30)
    name = models.CharField(verbose_name='Название лицензии',  max_length=20)
    dsc = models.TextField(verbose_name='Описание', default='Описание отсутствует', blank=True, null=True)
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    count_dialog = models.IntegerField(verbose_name='Количество диалогов', default=1)
    count_invited_user = models.IntegerField(verbose_name='Количество приглашенных пользователей')
    count_withdrawal = models.IntegerField(verbose_name='Вывод средств', default=30000)
    mess_ln = models.IntegerField(verbose_name='Длина сообщения')
    delay = models.IntegerField(verbose_name='Задержка', default=5)
    deg_protection = models.IntegerField(verbose_name='Степень защиты')
    name_license = models.CharField(verbose_name='Лицензия', choices=LICENSES_FIELD, max_length=20, default=LICENSES_FIELD[0])
    price = models.IntegerField(verbose_name='Стоимость', default=0, null=True, blank=True)
    price_update = models.IntegerField(verbose_name='Стоимость продления', default=0,)
    financial_constraints = models.ForeignKey('FinancialConstraints', verbose_name='Коммиссия на платежные операции',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class FinancialConstraints(models.Model):
    class Meta:
        verbose_name = 'Коммиссия'
        verbose_name_plural = 'Коммиссии'

    LICENSES_FIELD = [
        ("base", "Базовый"),
        ("base+", "Базовый+"),
        ('professionale', 'Для организаций'),
        ('professionale+', 'Для организаций+'),
        ("premium", "Партнерам"),
        ("premium+", "Партнерам+"),
        ("premium++", "Партнерам++"),
    ]

    name = models.CharField(verbose_name='Наименование', choices=LICENSES_FIELD, max_length=20)
    percentage_withdrawal = models.IntegerField(verbose_name='Процент на вывод')
    percentage_admission = models.IntegerField(verbose_name='Процент на пополнение')
    withdrawal_amount_min = models.IntegerField(verbose_name='Минимальная сумма вывода')
    withdrawal_amount_max = models.IntegerField(verbose_name='Максимальная сумма вывода')
    deposits_min = models.IntegerField(verbose_name='Минимальная сумма зачислений')
    deposits_max = models.IntegerField(verbose_name='Максимальная сумма зачислений')
    reward_ref = models.IntegerField(verbose_name='Вознаграждение за рефералов', default=1)

    def __str__(self):
        return self.name


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
    rif_token = models.CharField(verbose_name='Реферальный токен', max_length=20)
    photo = models.ImageField(verbose_name='Фотография', upload_to='user/photo/%Y/%m/%d/', null=True, blank=True)
    payments = models.ManyToManyField('Payment',  verbose_name='Платежные операции', null=True, blank=True)
    balance_tariff = models.ForeignKey('TariffBalances', verbose_name='Остаток тарифа', on_delete=models.PROTECT, null=True, blank=True)
    status_idf = models.CharField(verbose_name='Статус подключения', choices=STATUS_IDF_FIELDS, max_length=20, default='not_connect')
    identification_dialog = models.ForeignKey('ObjIdfDialog', verbose_name='Объект индификации диалога',  blank=True, null=True, on_delete=models.PROTECT)

    status_connection = models.ForeignKey('ConnectIDF', verbose_name='Статус подключения', on_delete=models.PROTECT,
                                          blank=True, null=True)
    internal_cash_account = models.IntegerField(verbose_name='Внутренний счет', default=0)
    technical_comment = models.CharField(verbose_name='Технический комментарий', max_length=20, blank=True, null=True)
    reference_user = models.ForeignKey('UserCustom', verbose_name='Реферанс', on_delete=models.PROTECT, blank=True, null=True)



class Flesh(models.Model):
    class Meta:
        verbose_name = 'Флешка'
        verbose_name_plural = 'Флешки'

    IDF = models.CharField(verbose_name='ИДФ', max_length=500)
    private_code = models.CharField(verbose_name='Приватный ключ', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активно', default=False)
    tariff = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.PROTECT)
    is_use_user = models.BooleanField(verbose_name='Используется?', default=False)
    count_flesh = models.IntegerField(verbose_name='Остаток флешек', default=0)
    price = models.IntegerField(verbose_name='Стоимость', default=0)
    auth_chat = models.BooleanField(verbose_name='Авторизация флешки', default=False)
    is_save_key = models.BooleanField(verbose_name='Локальное хранилище', default=False)

    def __str__(self):
        return self.IDF


class TariffBalances(models.Model):
    class Meta:
        verbose_name = 'Баланс тарифа'
        verbose_name_plural = 'Балансы тарифов'

    count_msg_user = models.IntegerField(verbose_name='Количество отправленных сообщений', default=0)
    count_invited_user = models.IntegerField(verbose_name='Количество приглашенных пользователей', default=1)
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    count_dialog = models.IntegerField(verbose_name='Количество диалогов', default=1)
    interlocutors = models.ManyToManyField(UserCustom, verbose_name='Собеседники', blank=True, null=True)
    count_withdrawal = models.IntegerField(verbose_name='Сумма вывода', default=1000)
    data_start = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    data_update = models.DateField(verbose_name='Дата обновления', auto_now=True)




class Payment(models.Model):
    class Meta:
        verbose_name = 'Платежная операция'
        verbose_name_plural = 'Платежные операции'

    CAT_FIELD = [
        ('purchase', 'Покупка'),
        ('update', 'Обновление'),
        ('purchase_bonuses', 'Оплата бонусами'),
        ('enrollment', 'Зачисление'),
        ('withdrawal', 'Вывод средств'),
        ('replenishment', 'Пополнение')
    ]

    STATUS_FIELD = [
        ('processing', 'В обработке'),
        ('checking', 'На проверке'),
        ('waiting', 'В ожидании'),
        ('successful', 'Успешный'),
        ('rejected', 'Отклонен'),
        ('return', 'Возврат'),
        ('unsuccessful', 'Неуспешный'),
        ('blocked', 'Заблокирован'),
        ('canceled', 'Отменен'),
        ('processed', 'Обработан'),
    ]

    category = models.CharField(verbose_name='Категория операции', max_length=30, choices=CAT_FIELD)
    dsc = models.CharField(verbose_name='Комментарий', max_length=155)
    price_start = models.IntegerField(verbose_name='Первоначальная цена', blank=True, null=True, default=0)
    percent_price = models.IntegerField(verbose_name='Процент операции', blank=True, null=True, default=0)
    price = models.IntegerField(verbose_name='Стоимость', default=0)
    status = models.CharField(verbose_name='Статус операции', max_length=30, choices=STATUS_FIELD,
                              default='waiting', blank=True, null=True)
    tech_msg = models.CharField(verbose_name='Внутренний комментарий', max_length=100, blank=True, null=True)
    date = models.DateTimeField(verbose_name='Дата операции', auto_now_add=True)
    technical_comment = models.CharField(verbose_name='Технический комментарий', max_length=20, blank=True, null=True)
    tariff = models.ForeignKey(Tariff, verbose_name='Приобретаемый тариф', on_delete=models.PROTECT, blank=True, null=True)
    reference = models.ForeignKey('UserCustom', verbose_name='Реферанс', on_delete=models.PROTECT, null=True, blank=True)


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


class CatNews(models.Model):
    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

    title = models.CharField(verbose_name='Категория', max_length=155)

    def __str__(self):
        return self.title


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
    subtitle = models.CharField(verbose_name='Подзаголовок', max_length=255)
    cat_status = models.CharField(verbose_name='Категория', choices=CAT_FIELD, max_length=20)
    image = models.ImageField(verbose_name='Превью', upload_to='news/%Y/%m/%d/', null=True, blank=True)
    category = models.ForeignKey('CatNews', verbose_name='Категория', on_delete=models.PROTECT)
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


class ConnectIDF(models.Model):
    class Meta:
        verbose_name = 'Статус подключения'
        verbose_name_plural = 'Статусы подключения'

    flesh_user = models.ForeignKey(Flesh, verbose_name='Время подключения', on_delete=models.PROTECT)
    is_connect = models.BooleanField(verbose_name='Статус')


class Support(models.Model):
    class Meta:
        verbose_name = 'Техподдержка'
        verbose_name_plural = 'Техподдержка'

    CAT_FIELD = [
        ('Problems_with_site', 'Проблемы с сайтом'),
        ('Problems_with_IDF', 'Проблема с IDF'),
        ('Problems_with_money', 'Финансовый вопрос'),
        ('Other', 'Иное')
    ]

    category = models.CharField(verbose_name='Категория', max_length=100, choices=CAT_FIELD)
    name = models.CharField(verbose_name='Имя', max_length=155)
    mail = models.EmailField(verbose_name='Почта', max_length=255)
    dsc = models.TextField(verbose_name='Обращение')
    data_start = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    data_end = models.DateField(verbose_name='Дата создания', null=True, blank=True)
    is_done = models.BooleanField(verbose_name='Решено', default=False)
from django.contrib.auth.models import AbstractUser
from django.db import models


class Tariff(models.Model):
    LICENSES_FIELD = [
        ("base", "Базовый"),
        ('professionale', 'Проффисиональный'),
        ("premium", "Преимум"),
    ]
    name = models.CharField(verbose_name='Название лицензии', default='none', max_length=20)
    mess_ln = models.IntegerField(verbose_name='Длина сообщения')
    delay = models.IntegerField(verbose_name='Задержка', default=5)
    count_msg = models.IntegerField(verbose_name='Количество сообщений')
    name_license = models.CharField(verbose_name='Лицензия', choices=LICENSES_FIELD, max_length=20, default=LICENSES_FIELD[0])

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    flesh = models.ForeignKey('Flesh', verbose_name='ID флешки', on_delete=models.CASCADE, default=None, null=True, blank=True)
    is_active_flesh = models.BooleanField(verbose_name='Активность аккаунта', default=True)
    rif_token = models.CharField(verbose_name='Реферальный токен', max_length=20, null=True, blank=True)
    photo = models.ImageField(verbose_name='Фотография', upload_to='user/photo/%Y/%m/%d/', null=True, blank=True)





class Flesh(models.Model):
    class Meta:
        verbose_name = 'Флешка'
        verbose_name_plural = 'Флешки'

    IDF = models.CharField(verbose_name='ИДФ', max_length=500)
    is_active = models.BooleanField(verbose_name='Активно', default=False)
    tariff = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.PROTECT)
    is_use_user = models.BooleanField(verbose_name='Используется?', default=False)

    def __str__(self):
        return self.IDF
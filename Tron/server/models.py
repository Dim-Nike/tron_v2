from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Tariff(models.Model):
    licenses = [
        ("base", "base"),

        ("premium", "premium"),
    ]
    name = models.CharField(verbose_name='Название лицензии', default='none', max_length=20)
    mess_ln = models.IntegerField(verbose_name='Длина сообщения')
    delay = models.IntegerField(verbose_name='Задержка', default=5)
    name_license = models.CharField(verbose_name='Лицензия', choices=licenses, max_length=10, default=licenses[0])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class User(AbstractBaseUser):
    login = models.CharField(verbose_name='Логин', max_length=150, unique=True)
    flesh = models.ForeignKey('Flesh', verbose_name='Флешка', on_delete=models.CASCADE, default=None)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Flesh(models.Model):

    IDF = models.CharField(verbose_name='ИДФ', max_length=500)
    is_active = models.BooleanField(verbose_name='Активно', default=False)
    tariff = models.ForeignKey(Tariff, verbose_name='Тариф', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Флешка'
        verbose_name_plural = 'Флешки'

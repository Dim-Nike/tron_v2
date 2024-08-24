from django.contrib.auth.models import AbstractUser
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name="название", unique=True, help_text='идентификатор комнаты (должен быть уникальным)')
    host = models.ForeignKey('server.ObjIdfDialog', on_delete=models.PROTECT, related_name="rooms", verbose_name="хозяин", help_text='Создатель комнаты')
    created_at = models.DateTimeField(verbose_name="дата создания чата")
    is_use = models.BooleanField(verbose_name='Используется', default=False)

    class Meta:
        verbose_name = "Частная комната"
        verbose_name_plural = "Частные комнаты"

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    room = models.ForeignKey("chat.Room", on_delete=models.PROTECT, related_name="messages", verbose_name="чат")
    text = models.TextField(max_length=500, verbose_name="текст")
    user = models.ForeignKey('server.UserCustom', on_delete=models.PROTECT, related_name="messages", verbose_name="Отправитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания", editable=True, )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"Message({self.user} {self.room})"

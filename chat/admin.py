# chat/admin.py

from django.contrib import admin

from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'created_at', 'is_use')
    list_filter = ('host', 'is_use')
    search_fields = ('name', 'host__username')
    readonly_fields = ('created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'text', 'user', 'created_at')
    list_filter = ('room', 'user')
    search_fields = ('room__name', 'text', 'user__username')
    readonly_fields = ('created_at',)

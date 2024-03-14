from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'IDF', 'tariff')  # Поля, которые будут отображаться в списке пользователей
    search_fields = ('login', 'IDF', 'tariff')  # Поля, по которым можно будет осуществлять поиск

admin.site.register(User, UserAdmin)
from django.contrib import admin
from .models import User

from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('login',)
    search_fields = ('login',)

class FleshAdmin(admin.ModelAdmin):
    list_display = ('IDF', 'tariff')
    search_fields = ('IDF', 'tariff')

class TariffAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Flesh, FleshAdmin)
admin.site.register(Tariff, TariffAdmin)

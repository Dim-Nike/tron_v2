from django.contrib import admin
from .models import *



class FleshAdmin(admin.ModelAdmin):
    list_display = ('IDF', 'tariff')
    search_fields = ('IDF', 'tariff')

class TariffAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(User)
admin.site.register(Flesh, FleshAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(TariffBalances)
admin.site.register(Payment)
admin.site.register(KeyIdentification)


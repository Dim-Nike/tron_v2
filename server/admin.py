from django.contrib import admin
from django.db.models import Count
from .models import *

class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_license', 'category_market', 'price', 'price_update')
    list_filter = ['name_license', 'category_market', ]
    search_fields = ('name',)


class UserCustomAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active_flesh')
    list_filter = ['is_active_flesh']


class FleshAdmin(admin.ModelAdmin):
    list_display = ('IDF', 'tariff', 'is_use_user', 'price', 'is_active')
    search_fields = ('IDF', 'tariff')
    list_filter = ['tariff', 'is_use_user', 'is_active']


class TariffBalancesAdmin(admin.ModelAdmin):
    list_display = ('count_msg_user', 'count_invited_user', 'count_msg', 'count_dialog',
                    'count_withdrawal', 'data_start', 'data_update')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('category', 'dsc', 'price', 'date')
    list_filter = ['category', 'date']


class KeyIdentificationAdmin(admin.ModelAdmin):
    list_display = ('token_dialog', 's_key', 'f_key', 'date_update', 'is_active')
    list_filter = ['is_active', 'date_update']


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date')
    list_filter = ['category', 'date']


class UserConnectFilter(admin.SimpleListFilter):
    title = 'User Connect'
    parameter_name = 'user_connect'

    def lookups(self, request, model_admin):
        return (
            ('no_users', 'No Connect'),
            ('one_user', 'Waiting'),
            ('two_users', 'Connect'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_users':
            return queryset.annotate(num_users=Count('user_connect')).filter(num_users=0)
        if self.value() == 'one_user':
            return queryset.annotate(num_users=Count('user_connect')).filter(num_users=1)
        if self.value() == 'two_users':
            return queryset.annotate(num_users=Count('user_connect')).filter(num_users=2)


class ObjIdfDialogAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'is_use', 'display_user_connect']
    list_filter = ['status', UserConnectFilter]

    def display_user_connect(self, obj):
        return ", ".join([user.username for user in obj.user_connect.all()])


class FinancialConstraintsAdmin(admin.ModelAdmin):
    list_display = ['name']


class SupportAdmin(admin.ModelAdmin):
    list_display = ['category', 'mail', 'data_start', 'is_done']
    list_filter = ['category', 'data_start', 'is_done']
    search_fields = ['mail']


admin.site.register(UserCustom, UserCustomAdmin)
admin.site.register(Flesh, FleshAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(TariffBalances, TariffBalancesAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(KeyIdentification, KeyIdentificationAdmin)
admin.site.register(CatNews)
admin.site.register(News, NewsAdmin)
admin.site.register(ObjIdfDialog, ObjIdfDialogAdmin)
admin.site.register(FinancialConstraints, FinancialConstraintsAdmin)
admin.site.register(Support, SupportAdmin)


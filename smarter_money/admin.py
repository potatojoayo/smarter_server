from django.contrib import admin

from smarter_money.models import Wallet, SmarterMoneyHistory, ChargeOrder, SmarterPaidHistory


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__gym__name', )


@admin.register(SmarterMoneyHistory)
class SmarterMoneyHistoryAdmin(admin.ModelAdmin):
    list_display = ('order_master', 'transaction_type', 'amount', 'date_created')
    search_fields = ('order_master__order_number', )


@admin.register(ChargeOrder)
class ChargeRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(SmarterPaidHistory)
class SmarterPaidHistoryAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from common.models import Card, Address, BankAccount, DeliveryAgency, Notification, Banner, Membership, \
    ExtraPriceDelivery, Notice, AddressZipCode


@admin.register(ExtraPriceDelivery)
class ExtraPriceDeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'title', 'contents', 'date_created')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryAgency)
class DeliveryAgencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass

@admin.register(AddressZipCode)
class AddressZipCodeAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'si_do', 'si_gun_gu', 'zip_code_start', 'zip_code_end', 'parent')
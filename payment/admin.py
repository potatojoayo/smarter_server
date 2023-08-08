from django.contrib import admin

from payment.models import PaymentFail, PaymentSuccess, TransferSuccess, CardSuccess, PaymentRequest
from payment.models.cancel_success import CancelSuccess
from payment.models.easypay_success import EasyPaySuccess


class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('amount', 'orderId', 'orderName', 'customerName', 'requestedAt')


class CardSuccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'number', 'installmentPlanMonths', 'approveNo', 'cardType', 'ownerType')


class TransferSuccessAdmin(admin.ModelAdmin):
    list_display = ('bank', 'settlementStatus')


class EasyPaySuccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'amount', 'discountAmount')


class CancelSuccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'cancelReason', 'canceledAt', 'cancelAmount', 'taxFreeAmount', 'taxAmount', 'transactionKey')


class PaymentSuccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderId', 'paymentKey', 'amount', 'approvedAt', 'status')


class PaymentFailAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'message', 'orderId')


admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(CardSuccess, CardSuccessAdmin)
admin.site.register(TransferSuccess, TransferSuccessAdmin)
admin.site.register(EasyPaySuccess, EasyPaySuccessAdmin)
admin.site.register(CancelSuccess, CancelSuccessAdmin)
admin.site.register(PaymentSuccess, PaymentSuccessAdmin)
admin.site.register(PaymentFail, PaymentFailAdmin)

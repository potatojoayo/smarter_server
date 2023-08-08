from django.contrib import admin

from class_payment.models.class_payment_master import ClassPaymentMaster
from class_payment.models.class_payment_request import ClassPaymentRequest
from class_payment.models.class_payment_success import ClassPaymentSuccess


@admin.register(ClassPaymentMaster)
class ClassPaymentMasterAdmin(admin.ModelAdmin):
    list_display = ('id','class_master', 'student', 'date_to')
    save_as = True


@admin.register(ClassPaymentRequest)
class ClassPaymentRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(ClassPaymentSuccess)
class ClassPaymentSuccessAdmin(admin.ModelAdmin):
    pass

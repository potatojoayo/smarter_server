from class_payment.models import ClassPaymentMaster


def run():
    ClassPaymentMaster.objects.filter(type=None).update(type="정기")
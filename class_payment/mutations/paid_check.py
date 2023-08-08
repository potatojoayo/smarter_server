import graphene
from datetime import datetime
from class_payment.models import ClassPaymentMaster


class PaidCheck(graphene.Mutation):
    class Arguments:
        class_payment_master_id = graphene.Int()
        method = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, class_payment_master_id, method):
        today = datetime.today().date()
        class_payment_master = ClassPaymentMaster.objects.get(pk=class_payment_master_id)
        class_payment_master.payment_method = method
        class_payment_master.payment_status = "납부완료"
        class_payment_master.date_paid = today
        class_payment_master.is_approved = True
        class_payment_master.save()

        return PaidCheck(success=True)

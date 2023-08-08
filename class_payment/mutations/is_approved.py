import datetime

import graphene
from dateutil import parser

from class_payment.methods.alarm_for_class_payment import alarm_for_class_payments_main
from class_payment.models import ClassPaymentMaster


class IsApproved(graphene.Mutation):
    class Arguments:
        class_payment_master_ids = graphene.List(graphene.Int)
        date = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _,info, class_payment_master_ids, date):
        print(class_payment_master_ids)
        gym_id = info.context.user.gym.id
        date = parser.parse(date)
        class_payment_masters = ClassPaymentMaster.objects.filter(pk__in=class_payment_master_ids)
        for class_payment_master in class_payment_masters:
            if class_payment_master.price_to_pay == 0 :
                class_payment_master.payment_status = "납부완료"
                class_payment_master.date_paid = datetime.date.today()
                class_payment_master_ids.remove(class_payment_master.id)
            class_payment_master.is_approved = True
            class_payment_master.save()
        # ClassPaymentMaster.objects.filter(pk__in=class_payment_master_ids).update(is_approved=True)
        print(class_payment_master_ids)
        alarm_for_class_payments_main(class_payment_master_ids, date, gym_id)
        return IsApproved(success=True)
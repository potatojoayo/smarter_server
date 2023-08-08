import graphene
from dateutil import parser

from class_payment.methods.alarm_for_class_payment import alarm_for_class_payments_main


class SendClassPaymentAlarm(graphene.Mutation):
    class Arguments:
        class_master_id = graphene.Int()
        date = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, **kwargs):
        class_master_id = kwargs.get('class_master_id')
        date = kwargs.get('date')
        date = parser.parse(date)
        gym_id = info.context.user.gym.id
        if class_master_id :
            pass
        else:
            class_master_id = -1

        alarm_for_class_payments_main(class_master_id, date, gym_id)

        return SendClassPaymentAlarm(success=True)
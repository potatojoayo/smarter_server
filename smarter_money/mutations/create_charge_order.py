import graphene
from datetime import datetime

from firebase_admin import messaging

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from smarter_money.models.charge_order import ChargeOrder
from smarter_money.types.charge_order_type import ChargeOrderType


class CreateChargeOrder(graphene.Mutation):
    class Arguments:
        amount = graphene.Int(required=True)
        method = graphene.String()

    charge_order = graphene.Field(ChargeOrderType)

    @classmethod
    def mutate(cls, _, info, amount, method=None):
        user = info.context.user
        now = datetime.now()

        state = '무통장입금' if method == '무통장입금' else '충전요청'

        charge_order = ChargeOrder.objects.create(user=user,
                                                  order_id='S{}{}'.format(user.phone, now.strftime('%y%m%d%H%M%S')),
                                                  amount=amount, state=state, method=method
                                                  )

        if method == '무통장입금':
            send_notification(user=user, type="무통장입금안내", amount=amount)

        return CreateChargeOrder(charge_order=charge_order)

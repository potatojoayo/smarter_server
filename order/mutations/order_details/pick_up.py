from datetime import datetime

import graphene

from order.models import OrderDetail, OrderMaster
from smarter_money.models import SmarterMoneyHistory


class PickUp(graphene.Mutation):
    class Arguments:
        order_master_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_master_ids):
        order_masters = OrderMaster.objects.filter(pk__in=order_master_ids)
        for order_master in order_masters:
            order_master.details.update(state="방문수령")
            user = order_master.user
            user.wallet.balance += order_master.price_delivery
            user.wallet.save()
            SmarterMoneyHistory.objects.create(
                order_master=order_master,
                history_number='V{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=user.wallet,
                transaction_type='적립',
                amount=order_master.price_delivery,
                description='{} 방문수령'.format(order_master.order_name)
            )
        return PickUp(success=True)


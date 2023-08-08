from datetime import datetime
import graphene
from django.db import transaction

from authentication.models import User
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from smarter_money.models import SmarterMoneyHistory, ChargeOrder
from smarter_money.types.charge_smarter_money_input_type import ChargeSmarterMoneyInputType


class BulkChargeSmarterMoney(graphene.Mutation):
    class Arguments:
        orders = graphene.List(ChargeSmarterMoneyInputType)

    success_count = graphene.Int()

    @classmethod
    def mutate(cls, _, __, orders):
        print(orders)
        success_count = 0
        for order in orders:
            with transaction.atomic():
                user = User.objects.get(pk=order.user_id)

                charge_order = ChargeOrder.objects.get(pk=order.order_id)
                wallet = user.wallet
                wallet.balance += charge_order.amount

                SmarterMoneyHistory.objects.create(
                    history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                    wallet=wallet,
                    transaction_type='충전',
                    amount=charge_order.amount,
                    description=charge_order.order_name
                )

                wallet.save()

                charge_order.state = '결제완료'
                charge_order.save()

                """title = '스마터머니 충전 완료'
                contents = '스마터머니 {:0,.0f}원이 충전되었습니다.'.format(charge_order.amount)
                create_notification(notification_type='충전',
                                    title=title,
                                    contents=contents,
                                    user=user,
                                    route='/smarter-money'
                                    )
                """
                #send_notification(user=user, type="충전", amount=charge_order.amount)
                success_count += 1

        return BulkChargeSmarterMoney(success_count=success_count)



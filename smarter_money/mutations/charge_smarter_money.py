from datetime import datetime
import graphene
from django.db import transaction

from authentication.models import User
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from smarter_money.models import SmarterMoneyHistory, ChargeOrder
from smarter_money.types.smarter_money_history_type import SmarterMoneyHistoryType
from smarter_money.types.wallet_type import WalletType


class ChargeSmarterMoney(graphene.Mutation):
    class Arguments:
        order_id = graphene.String()
        user_id = graphene.Int()

    wallet = graphene.Field(WalletType)
    smarter_money_history = graphene.Field(SmarterMoneyHistoryType)
    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, info, order_id, user_id=None):
        with transaction.atomic():
            if user_id:
                user = User.objects.get(pk=user_id)
            else:
                user = info.context.user
            charge_order = ChargeOrder.objects.get(pk=order_id)

            wallet = user.wallet
            wallet.balance += charge_order.amount

            smarter_money_history = SmarterMoneyHistory.objects.create(
                history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=wallet, transaction_type='충전', amount=charge_order.amount, description='스마터머니 충전'
            )

            wallet.save()

            charge_order.state = '결제완료'
            charge_order.save()

            #send_notification(user=user, type="충전", amount=charge_order.amount)
            return ChargeSmarterMoney(wallet=wallet, smarter_money_history=smarter_money_history, success=True)



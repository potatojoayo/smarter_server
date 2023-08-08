from datetime import datetime

import graphene
from django.db import transaction

from authentication.models import User
from smarter_money.models import SmarterMoneyHistory


class CsChargeSmarterMoney(graphene.Mutation):
    """
    고객 문의로 인한 스마터머니 충전. \n
    description이 null 이면 '고객문의로 인한 충전'으로 세팅
    """
    class Arguments:
        user_id = graphene.Int(required=True)
        amount = graphene.Int(required=True)
        description = graphene.String()

    success = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, user_id, amount, description=None):
        try:
            user = User.objects.get(pk=user_id)
            wallet = user.wallet
            wallet.balance += amount
            wallet.save()
            SmarterMoneyHistory.objects.create(
                history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=wallet,
                transaction_type='충전',
                amount=amount,
                description=description if description else '고객문의로 인한 충전'
            )
            return CsChargeSmarterMoney(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CsChargeSmarterMoney()




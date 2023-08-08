from datetime import datetime

import graphene
from django.db import transaction

from authentication.models import User
from smarter_money.models import SmarterMoneyHistory


class CsSubtractSmarterMoney(graphene.Mutation):
    """
    TODO
    고객 문의로 인한 스마터머니 차감. \n
    """
    class Arguments:
        user_id = graphene.Int(required=True)
        amount = graphene.Int(required=True)
        description = graphene.String()

    success = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __,
               user_id,
               amount,
               description=''):
        try:
            user = User.objects.get(pk=user_id)
            wallet = user.wallet
            wallet.balance -= amount
            wallet.save()
            SmarterMoneyHistory.objects.create(
                history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=wallet,
                transaction_type='차감',
                amount=amount,
                description=description
            )
            return CsSubtractSmarterMoney(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CsSubtractSmarterMoney()




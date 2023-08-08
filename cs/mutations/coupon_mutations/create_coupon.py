from datetime import datetime

import graphene
from django.db import transaction

from cs.models import CouponMaster


class CreateCouponMaster(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        price = graphene.Int()
        message = graphene.String()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        try:
            name = kwargs.get('name')
            price = kwargs.get('price')
            message = kwargs.get('message')
            CouponMaster.objects.create(name=name, price=price,  type='수동쿠폰', coupon_message=message, )
            return CreateCouponMaster(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateCouponMaster(success=False)

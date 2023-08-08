import math

import graphene

from business.models import Gym
from common.models import Address
from common.types import AddressType
from cs.types.addresses_type import AddressesType


class CreateAddress(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int()
        name = graphene.String()
        receiver = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        is_default = graphene.Boolean()
        delivery_memo = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym_id, **kwargs):
        try:
            gym = Gym.objects.get(pk=gym_id)
            user = gym.user
            name = kwargs.get('name')
            receiver = kwargs.get('receiver')
            email = kwargs.get('email')
            phone = kwargs.get('phone')
            zip_code = kwargs.get('zip_code')
            address = kwargs.get('address')
            detail_address = kwargs.get('detail_address')
            memo = kwargs.get('delivery_memo')
            default = kwargs.get('is_default')

            if default:
                user.addresses.all().update(default=False)
            Address.objects.create(user=user,
                                   name=name,
                                   receiver=receiver,
                                   email=email,
                                   phone=phone,
                                   zip_code=zip_code,
                                   address=address,
                                   detail_address=detail_address,
                                   default=default,
                                   delivery_memo=memo)
            return CreateAddress(success=True,)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateAddress(success=False)

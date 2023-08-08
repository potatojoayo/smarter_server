import graphene
from django.db import transaction

from business.models import Gym
from common.models import Address
from cs.types.input_types.address_input_type import AddressInputType


class CreateOrUpdateUserAddress(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int()
        default_address_id = graphene.Int()
        added_address = AddressInputType()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, gym_id, default_address_id, added_address):
        try:
            gym = Gym.objects.get(pk=gym_id)
            user = gym.user
            default_address = Address.objects.filter(pk=default_address_id)
            if default_address :
                default_address.update(default=True)
                if added_address.address :
                    Address.objects.create(user=user,
                                           name=added_address.name,
                                           receiver=added_address.receiver,
                                           phone=added_address.phone,
                                           address=added_address.address,
                                           detail_address=added_address.address,
                                           default=True)
            else:
                user.addresses.all().update(default=False)
                Address.objects.create(user=user,
                                       name=added_address.name,
                                       receiver=added_address.receiver,
                                       phone=added_address.phone,
                                       address=added_address.address,
                                       detail_address=added_address.address,
                                       default=True)
            return CreateOrUpdateUserAddress(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateOrUpdateUserAddress(success=False)



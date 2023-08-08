import graphene

from authentication.models import User
from common.models import Address
from common.types import AddressType
from cs.types.input_types.address_input_type import AddressInputType


class SelectAddress(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int()
        new_address = AddressInputType()

    success = graphene.Boolean()
    selected_address = graphene.Field(AddressType)
    @classmethod
    def mutate(cls, _, __, **kwargs):
        try:
            address_id = kwargs.get('address_id')
            new_address = kwargs.get('new_address')
            if address_id:
                selected_address = Address.objects.get(pk=address_id)
                return SelectAddress(success=True, selected_address=selected_address)
            else:
                user = User.objects.get(pk=new_address.user_id)
                new_address = Address.objects.create(user=user,
                                                     name=user.name,
                                                     receiver=new_address.receiver,
                                                     phone=new_address.phone,
                                                     address=new_address.address,
                                                     detail_address=new_address.detail_address,
                                                     zip_code=new_address.zip_code)
                return SelectAddress(success=True, selected_address=new_address)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return SelectAddress(success=False)
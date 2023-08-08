import graphene

from authentication.models import User
from common.models import Address
from common.types import AddressType


class CreateOrUpdateAddress(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int()
        user_id = graphene.Int()
        address_name = graphene.String()
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        default = graphene.Boolean()

    success = graphene.Boolean()
    address = graphene.Field(AddressType)

    @classmethod
    def mutate(cls, _, info, address_name, receiver, phone, zip_code, address, detail_address, default, user_id=None,
               address_id=None, ):

        if not user_id:
            user = info.context.user
        else:
            user = User.objects.get(pk=user_id)

        if default:
            user.addresses.all().update(default=False)

        if address_id:
            address = Address.objects.filter(pk=address_id).update(user=user, name=address_name,
                                                         address=address,
                                                         receiver=receiver,
                                                         phone=phone,
                                                         zip_code=zip_code,
                                                         detail_address=detail_address,
                                                         default=default
                                                         )
        else:
            address = Address.objects.create(user=user, name=address_name,
                                   address=address,
                                   receiver=receiver,
                                   phone=phone,
                                   zip_code=zip_code,
                                   detail_address=detail_address,
                                   default=default
                                   )

        return CreateOrUpdateAddress(success=True, address=address)

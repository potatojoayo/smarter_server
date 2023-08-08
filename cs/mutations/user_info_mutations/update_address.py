import graphene

from common.models import Address
from common.types import AddressType


class UpdateAddress(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int()
        name = graphene.String()
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        is_default = graphene.Boolean()
        delivery_memo = graphene.String()
        page = graphene.Int()

    success = graphene.Boolean()
    addresses = graphene.List(AddressType)

    @classmethod
    def mutate(cls, _, __, address_id, **kwargs):
        try:
            updated_address = Address.objects.get(pk=address_id)
            name = kwargs.get('name')
            receiver = kwargs.get('receiver')
            phone = kwargs.get('phone')
            zip_code = kwargs.get('zip_code')
            address = kwargs.get('address')
            detail_address = kwargs.get('detail_address')
            delivery_memo = kwargs.get('delivery_memo')
            default = kwargs.get('is_default')
            page = kwargs.get('page')

            if default:
                updated_address.user.addresses.all().update(default=False)
            updated_address.name = name
            updated_address.receiver = receiver
            updated_address.phone = phone
            updated_address.zip_code = zip_code
            updated_address.address = address
            updated_address.detail_address = detail_address
            updated_address.delivery_memo = delivery_memo
            updated_address.default = default
            updated_address.save()

            user = updated_address.user

            addresses = user.addresses.filter(is_deleted=False).order_by('-id')[(page-1)*10: page*10]

            return UpdateAddress(success=True, addresses=addresses)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateAddress(success=False)

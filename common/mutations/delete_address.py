import graphene

from common.models import Address


class DeleteAddress(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int(required=True)

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, address_id):
        try:
            address = Address.objects.get(pk=address_id)
            if address.default:
                return DeleteAddress(message='기본 배송지는 삭제할 수 없습니다.')
            Address.objects.filter(pk=address_id).update(is_deleted=True)
            return DeleteAddress(success=True)
        except:
            return DeleteAddress()

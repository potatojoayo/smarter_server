import graphene

from order.models import ZipCode


class CreateOrUpdateAdditionalDeliveryPrice(graphene.Mutation):
    class Arguments:
        zip_code_id = graphene.Int()
        zip_code = graphene.String()
        address = graphene.String()
        additional_delivery_price = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, **kwargs):
        zip_code_id = kwargs.get('zip_code_id')
        zip_code = kwargs.get('zip_code')
        address = kwargs.get('address')
        additional_delivery_price = kwargs.get('additional_delivery_price')

        if zip_code_id:
            ZipCode.objects.filter(pk=zip_code_id).update(zip_code=zip_code,
                                                          address=address,
                                                          additional_delivery_price=additional_delivery_price)
        else:
            ZipCode.objects.create(zip_code=zip_code,
                                   address=address,
                                   additional_delivery_price=additional_delivery_price)

        return CreateOrUpdateAdditionalDeliveryPrice(success=True)

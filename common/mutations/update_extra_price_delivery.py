import graphene

from common.models import ExtraPriceDelivery
from order.models import ZipCode


class UpdateExtraPriceDelivery(graphene.Mutation):
    class Arguments:
        price = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, price):
        ExtraPriceDelivery.objects.all().update(price=price)
        ZipCode.objects.all().update(additional_delivery_price=price)
        return UpdateExtraPriceDelivery(success=True)

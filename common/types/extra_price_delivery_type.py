from graphene_django import DjangoObjectType

from common.models import ExtraPriceDelivery


class ExtraPriceDeliveryType(DjangoObjectType):
    class Meta:
        model = ExtraPriceDelivery


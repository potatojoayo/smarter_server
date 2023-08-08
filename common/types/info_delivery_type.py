from graphene_django import DjangoObjectType

from common.models.info_delivery import InfoDelivery


class InfoDeliveryType(DjangoObjectType):
    class Meta:
        model = InfoDelivery

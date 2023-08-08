from graphene_django import DjangoObjectType

from common.models import DeliveryAgency


class DeliveryAgencyType(DjangoObjectType):

    class Meta:
        model = DeliveryAgency
        
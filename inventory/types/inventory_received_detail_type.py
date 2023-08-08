from graphene_django import DjangoObjectType

from inventory.models import InventoryReceivedDetail


class InventoryReceivedDetailType(DjangoObjectType):
    class Meta:
        model = InventoryReceivedDetail


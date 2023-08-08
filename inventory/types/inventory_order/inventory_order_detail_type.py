from graphene_django import DjangoObjectType

from inventory.models import InventoryOrderDetail


class InventoryOrderDetailType(DjangoObjectType):
    class Meta:
        model = InventoryOrderDetail

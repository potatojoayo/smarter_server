from graphene_django import DjangoObjectType

from inventory.models import InventoryOrderMaster


class InventoryOrderMasterType(DjangoObjectType):
    class Meta:
        model = InventoryOrderMaster

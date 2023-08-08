
from graphene_django import DjangoObjectType

from inventory.models import InventoryReceivedMaster


class InventoryReceivedMasterType(DjangoObjectType):
    class Meta:
        model = InventoryReceivedMaster

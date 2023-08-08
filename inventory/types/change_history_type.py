from graphene_django import DjangoObjectType

from inventory.models import ChangeHistory


class ChangeHistoryType(DjangoObjectType):
    class Meta:
        model = ChangeHistory

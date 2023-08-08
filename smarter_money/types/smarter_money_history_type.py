import graphene
from graphene_django import DjangoObjectType

from smarter_money.models import SmarterMoneyHistory


class SmarterMoneyHistoryType(DjangoObjectType):

    class Meta:
        model = SmarterMoneyHistory

    order_number = graphene.String()

    @staticmethod
    def resolve_order_number(root, _):
        if root.order_master:
            return root.order_master.order_number


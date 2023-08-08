import graphene

from smarter_money.types.smarter_money_history_type import SmarterMoneyHistoryType


class SmarterMoneyHistories(graphene.ObjectType):

    list = graphene.List(SmarterMoneyHistoryType)
    total_count = graphene.Int()

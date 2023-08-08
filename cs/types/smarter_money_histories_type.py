import graphene

from smarter_money.types.smarter_money_history_type import SmarterMoneyHistoryType


class SmarterMoneyHistoriesType(graphene.ObjectType):
    smarter_money_histories = graphene.List(SmarterMoneyHistoryType)
    total_count = graphene.Int()
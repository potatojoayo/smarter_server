import graphene

from cs.types.partial_cancel_history_type import PartialCancelHistoryType


class PartialCancelHistoriesType(graphene.ObjectType):

    partial_cancel_histories = graphene.List(PartialCancelHistoryType)
    total_count = graphene.Int()


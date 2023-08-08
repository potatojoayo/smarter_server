import graphene
from django.db import transaction

from order.models import EasyOrder


class DeleteEasyOrderRequests(graphene.Mutation):
    class Arguments:
        easy_order_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, easy_order_ids):
        EasyOrder.objects.filter(pk__in=easy_order_ids).update(state='삭제')
        print('yes')
        return DeleteEasyOrderRequests(success=True)

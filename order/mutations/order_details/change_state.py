# 각 상태(state)를 바꿔주는 mutation

import graphene
from django.db import transaction

from order.models import OrderDetail


class ChangeState(graphene.Mutation):
    class Arguments:
        order_detail_numbers = graphene.List(graphene.String)
        state = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_detail_numbers, state):
        order_details = OrderDetail.objects.filter(order_detail_number__in=order_detail_numbers)
        order_details.update(state=state)
        return ChangeState(success=True)

import graphene
from django.db import transaction

from order.models import OrderDetail, EasyOrder


class CancelEasyOrder(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_master_id):
        easy_order = EasyOrder.objects.get(order=order_master_id)
        easy_order.state = '주문요청'
        easy_order.order = None
        easy_order.save()
        OrderDetail.objects.filter(order_master_id=order_master_id).update(state='간편주문취소')
        return CancelEasyOrder(success=True)
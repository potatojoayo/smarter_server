import graphene
from django.db import transaction

from order.methods.order_details_automation import order_details_automation
from order.models import OrderDetail, OrderMaster


class ProceedPaidOrders(graphene.Mutation):
    class Arguments:
        order_master_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_master_ids):
        order_masters = OrderMaster.objects.filter(pk__in=order_master_ids)
        for order_master in order_masters:
            order_details = OrderDetail.objects.filter(order_master=order_master, state="결제완료")
            order_details_automation(order_details, order_master)
            for child in order_master.children.all():
                order_details = OrderDetail.objects.filter(order_master=child, state='결제완료')
                order_details_automation(order_details, child)

        return ProceedPaidOrders(success=True)

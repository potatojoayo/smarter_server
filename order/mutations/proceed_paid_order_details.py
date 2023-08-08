import graphene

from order.methods.order_details_automation import order_details_automation
from order.models import OrderDetail, OrderMaster


class ProceedPaidOrderDetails(graphene.Mutation):
    class Arguments:
        order_detail_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_detail_ids):
        order_details = OrderDetail.objects.filter(pk__in=order_detail_ids, state="추후배송")
        order_master_dic = {}
        for order_detail in order_details:
            value = order_master_dic.get(order_detail.order_master.id)
            if value is None:
                order_master_dic[order_detail.order_master.id] = [order_detail]
            else:
                order_master_dic[order_detail.order_master.id].append(order_detail)
        for order_master_id, order_details in order_master_dic.items():
            order_master = OrderMaster.objects.get(pk=order_master_id)
            order_details_automation(order_details, order_master)

        return ProceedPaidOrderDetails(success=True)

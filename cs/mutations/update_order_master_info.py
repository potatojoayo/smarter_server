import graphene

from order.models import OrderMaster


class UpdateOrderMasterInfo(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int()
        delivery_request = graphene.String()
        is_pick_up = graphene.Boolean()
        memo_by_admin = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_master_id, **kwargs):
        try:
            order_master = OrderMaster.objects.get(pk=order_master_id)
            delivery_request = kwargs.get('delivery_request')
            is_pick_up = kwargs.get('is_pick_up')
            memo_by_admin = kwargs.get('memo_by_admin')
            if delivery_request :
                order_master.delivery_request = delivery_request
            elif is_pick_up :
                order_master.is_pick_up = is_pick_up
            else :
                order_master.memo_by_admin = memo_by_admin
            order_master.save()

            return UpdateOrderMasterInfo(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateOrderMasterInfo(success=False)

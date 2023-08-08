import graphene

from order.models import TaOrderMaster, TaOrderDetail
from order.types.ta.ta_order_detail_input_type import TaOrderDetailInputType


class UpdateTaOrder(graphene.Mutation):
    class Arguments:
        ta_order_master_id = graphene.Int()
        ta_order_details = graphene.List(TaOrderDetailInputType)
        price_paid = graphene.Int()
        price_delivery = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, ta_order_master_id, ta_order_details, price_paid, price_delivery):
        try:
            ta_order_master = TaOrderMaster.objects.get(pk=ta_order_master_id)
            for ta_order_detail in ta_order_details:
                old_ta_order_detail = TaOrderDetail.objects.get(pk=ta_order_detail.id)
                old_ta_order_detail.price_special = ta_order_detail.price_special
                old_ta_order_detail.total_price_special = ta_order_detail.price_special * old_ta_order_detail.order_detail.quantity
                old_ta_order_detail.save()

            ta_order_master.price_paid = price_paid
            ta_order_master.price_delivery = price_delivery
            ta_order_master.price_to_be_paid = ta_order_master.total_price_special - price_paid + price_delivery
            if ta_order_master.price_to_be_paid <= 0 :
                ta_order_master.is_paid = True
            ta_order_master.save()

            return UpdateTaOrder(success=True, message="수정되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info('update_ta_order 뮤테이션')
            logger.info(e)
            return UpdateTaOrder(success=False, message="오류가 발생하였습니다.")
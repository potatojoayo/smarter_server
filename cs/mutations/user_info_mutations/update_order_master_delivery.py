import graphene

from common.models import Address
from order.models import Delivery, OrderMaster


class UpdateOrderMasterDelivery(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int()
        order_master_id = graphene.Int()
    success = graphene.Int()

    @classmethod
    def mutate(cls, _, __, address_id, order_master_id):
        try:
            address = Address.objects.get(pk=address_id)
            order_master = OrderMaster.objects.get(pk=order_master_id)

            order_master.receiver = address.receiver
            order_master.email = address.email
            order_master.phone = address.phone
            order_master.zip_code = address.zip_code
            order_master.address = address.address
            order_master.detail_address = address.detail_address
            order_master.save()
            return UpdateOrderMasterDelivery(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateOrderMasterDelivery(success=False)
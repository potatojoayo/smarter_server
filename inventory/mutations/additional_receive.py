import graphene
from datetime import datetime

from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from common.models import Notification
from inventory.models import InventoryOrderDetail, InventoryReceivedMaster, InventoryReceivedDetail, ChangeHistory
from inventory.types.additional_receive_input_type import AdditionalReceiveInputType
from inventory.models import ChangeHistory


class AdditionalReceive(graphene.Mutation):
    class Arguments:
        inventory_received_details = graphene.List(AdditionalReceiveInputType)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, inventory_received_details):
        master = None
        for detail_input in inventory_received_details:
            detail = InventoryReceivedDetail.objects.get(pk=detail_input.id)
            detail.quantity_additional_received = detail_input.quantity_additional_received
            detail.price_additional_received = detail.price_vendor * detail.quantity_additional_received
            detail.save()
            master = detail.inventory_received_master
            product = detail.inventory_order_detail.product
            ChangeHistory.objects.create(product_master=product.product_master,
                                         product=product,
                                         quantity_before=product.inventory_quantity,
                                         quantity_after=product.inventory_quantity + detail.quantity_additional_received,
                                         quantity_changed=detail.quantity_additional_received,
                                         reason='추가입고')
        master.state = '종결'
        master.save()
        

        return AdditionalReceive(success=True)



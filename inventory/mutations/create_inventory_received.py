import graphene
from datetime import datetime

from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from common.models import Notification
from inventory.models import InventoryOrderDetail, InventoryReceivedMaster, InventoryReceivedDetail, ChangeHistory
from inventory.types.inventory_received_input_type import InventoryReceivedInputType


class CreateInventoryReceived(graphene.Mutation):
    class Arguments:
        inventory_received_details = graphene.List(InventoryReceivedInputType)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, inventory_received_details):
        inventory_ordered_detail_id = inventory_received_details[0].inventory_order_detail_id
        inventory_order_detail = InventoryOrderDetail.objects.get(pk=inventory_ordered_detail_id)
        inventory_order_master = inventory_order_detail.inventory_order_master
        number = 'R{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
        inventory_received_master = InventoryReceivedMaster.objects.create(receive_number=number, inventory_order_master=inventory_order_master)
        completed_number = 0

        for inventory_received_detail in inventory_received_details:
            inventory_ordered_detail = InventoryOrderDetail.objects.get(pk=inventory_received_detail.inventory_order_detail_id)
            name = inventory_ordered_detail.name
            color = inventory_ordered_detail.color
            size = inventory_ordered_detail.size
            price_vendor = inventory_ordered_detail.price_vendor
            quantity_ordered = inventory_ordered_detail.quantity_ordered
            price_ordered = inventory_ordered_detail.quantity_ordered * price_vendor
            quantity_received = inventory_received_detail.quantity_received
            quantity_not_received = inventory_received_detail.quantity_not_received
            price_received = price_vendor * quantity_received

            product = inventory_ordered_detail.product

            ChangeHistory.objects.create(product_master=product.product_master,
                                         product=product,
                                         quantity_before=product.inventory_quantity,
                                         quantity_after=product.inventory_quantity + quantity_received,
                                         quantity_changed=quantity_received,
                                         reason='입고')

            product.inventory_quantity += quantity_received
            if product.inventory_quantity <= 0:
                product.lack_inventory = True
            else:
                product.lack_inventory = False
            product.save()

            InventoryReceivedDetail.objects.create(inventory_order_detail=inventory_ordered_detail,
                                                   inventory_received_master=inventory_received_master,
                                                   name=name,
                                                   color=color,
                                                   size=size,
                                                   price_vendor=price_vendor,
                                                   quantity_ordered=quantity_ordered,
                                                   price_ordered=price_ordered,
                                                   quantity_received=quantity_received,
                                                   quantity_not_received=quantity_not_received,
                                                   price_received=price_received,
                                                   reason_not_received=inventory_received_detail.reason
                                                   )


            if quantity_not_received == 0:
                completed_number += 1
                admin = Group.objects.get(name="관리자")
                admin_users = User.objects.filter(groups=admin)
                for admin_user in admin_users:
                    Notification.objects.create(user=admin_user, title="입고완료 알림",
                                                contents="{}상품이 입고완료되었습니다."
                                                .format(inventory_order_detail.product.name),
                                                notification_type="입고완료")
            else:
                admin = Group.objects.get(name="관리자")
                admin_users = User.objects.filter(groups=admin)
                for admin_user in admin_users:
                    Notification.objects.create(user=admin_user, title="부분입고완료 알림",
                                                contents="{}상품이 부분 입고완료되었습니다. 미입고 상품확인 부탁드립니다."
                                                .format(inventory_order_detail.product.name),
                                                notification_type="부분입고완료")
        if completed_number == len(inventory_received_details):
            inventory_order_master.state = '종결'
            inventory_order_master.save()
            inventory_received_master.state = "종결"
            inventory_received_master.save()
        else:
            inventory_order_master.state = '부분종결'
            inventory_order_master.save()
            inventory_received_master.state = "부분종결"
            inventory_received_master.save()

        return CreateInventoryReceived(success=True)



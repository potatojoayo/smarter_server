import graphene
from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from common.methods.create_notification import create_notification
from common.models import Notification
from inventory.models import ChangeHistory
from product.models import Product


class ChangeInventoryQuantity(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        reason = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, product_id, quantity, reason):
        product = Product.objects.get(pk=product_id)
        product_master = product.product_master
        quantity_before = product.inventory_quantity
        product.inventory_quantity = quantity
        if product.inventory_quantity <= 0:
            product.lack_inventory = True
        else:
            product.lack_inventory = False
        product.save()
        ChangeHistory.objects.create(product_master=product_master,
                                     product=product,
                                     quantity_before=quantity_before,
                                     quantity_after=product.inventory_quantity,
                                     quantity_changed=quantity,
                                     reason=reason)

        admin = Group.objects.get(name="관리자")
        admin_users = User.objects.filter(groups=admin)
        for admin_user in admin_users:
            Notification.objects.create(user=admin_user, title='임의재고수량변경', contents='{}이 관리자의 의해 재고 수량이 변경되었습니다.'
                                        .format(product.name), notification_type='임의재고수량 변경')
        return ChangeInventoryQuantity(success=True)

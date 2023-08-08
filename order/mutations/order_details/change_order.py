import graphene

from inventory.models import ChangeHistory
from order.models import OrderDetail
from product.models import Product


class ChangeOrder(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int(required=True)
        new_product_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)
        reason = graphene.String(required=True)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_detail_id, new_product_id, quantity, reason):
        order_detail = OrderDetail.objects.get(pk=order_detail_id)

        old_product_id = order_detail.product_id
        old_product = order_detail.product
        old_product_master = order_detail.product_master

        new_product = Product.objects.get(pk=new_product_id)
        new_product_master = new_product.product_master

        changed_quantity = quantity

        # 교환했을때 해당 order_detail에 해당되는 product의 갯수를 증가시켜준다.

        old_quantity_before = old_product.inventory_quantity
        old_quantity_after = old_product.inventory_quantity+changed_quantity
        quantity_changed_in = changed_quantity
        Product.objects.filter(pk=old_product_id).update(inventory_quantity=old_quantity_after)
        ChangeHistory.objects.create(order_detail=order_detail, product_master=old_product_master,product=old_product,
                                     quantity_before=old_quantity_before, quantity_after=old_quantity_after,
                                     quantity_changed_in=quantity_changed_in, reason=reason)
        #order_detail의 바꾼 product로 바꿔준다
        OrderDetail.objects.filter(pk=order_detail_id).update(product=new_product, product_master=new_product_master)
        #새로 선택한 product의 갯수를 감소시켜준다.
        #order_detail에 새로운 product를 넣어줌
        new_quantity_before = new_product.inventory_quantity
        new_quantity_after = new_product.inventory_quantity - changed_quantity
        if new_quantity_after <= 0:
            lack_inventory = True
        else:
            lack_inventory = False
        new_product.save()
        quantity_changed_out = changed_quantity
        Product.objects.filter(pk=new_product_id).update(inventory_quantity=new_quantity_after, lack_inventory=lack_inventory)
        ChangeHistory.objects.create(order_detail=order_detail, product_master=new_product_master,product=new_product,
                                     quantity_before=new_quantity_before, quantity_after=new_quantity_after, quantity_changed_out=quantity_changed_out)
        return ChangeOrder(success=True)

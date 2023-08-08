# 교환요청에서 교환완료 됬을때 mutation
# order_detail 각각 처리해야된다 -> order detail의 해당 product의 inventory quantity를 증가시킨다
import graphene

from inventory.models import ChangeHistory
from order.models import OrderDetail, ZipCode
from order.types.zip_code_type import ZipCodeType
from product.models import Product


class RefundOrder(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int(required=True)
        reason = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, order_detail_id, reason):
        order_detail = OrderDetail.objects.get(pk=order_detail_id)
        product_id = order_detail.product_id
        product = Product.objects.get(pk=product_id)
        OrderDetail.objects.filter(pk=order_detail_id).update(state="반품완료")
        quantity_before = product.inventory_quantity
        quantity_after = product.inventory_quantity + order_detail.quantity
        quantity_returned = order_detail.quantity
        if quantity_after <= 0:
            lack_inventory = True
        else:
            lack_inventory = False
        Product.objects.filter(pk=product_id).update(inventory_quantity=product.inventory_quantity+order_detail.quantity, lack_inventory=lack_inventory)
        # ChangeHistory.objects.create(order_detail=order_detail, product_master=product.product_master, product=product,
        #                              quantity_before=quantity_before,
        #                              quantity_after=quantity_after, quantity_returned=quantity_returned, reason=reason)

        #zip_code test용
        """price = ZipCode.objects.filter(zip_code=zip_code).first()
        if price:
            print(price.cost)
        else:
            print(123)
        return RefundOrder(success=True)
        """
        return RefundOrder(success=True)
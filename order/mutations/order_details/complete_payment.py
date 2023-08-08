from datetime import datetime

import graphene
from django.db import transaction

from inventory.models import ChangeHistory
from order.methods.belt_assign_work import belt_assign_work
from order.methods.delivery import delivery
from order.models import OrderMaster
from order.models.order_detail import OrderDetail
from order.types.order_master_type import OrderMasterType
from product.models import Product
from smarter_money.models import SmarterMoneyHistory


class CompletePayment(graphene.Mutation):

    class Arguments:
        order_id = graphene.Int()
        order_number = graphene.String()
        receiver = graphene.String()
        phone = graphene.String()
        zip_code = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        delivery_request = graphene.String()
        smarter_money = graphene.Int()

    success = graphene.Boolean()
    order_master = graphene.Field(OrderMasterType)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info,
               receiver,
               phone,
               zip_code,
               address,
               detail_address=None,
               delivery_request=None,
               smarter_money=None,
               order_id=None,
               order_number=None,
               ):
        if order_number is None:
            order_master = OrderMaster.objects.get(pk=order_id)
        else:
            order_master = OrderMaster.objects.get(order_number=order_number)
        # 결제완료되었을때 order_master에 해당되는 모든 order detail을 결제완료로 표시하기


        OrderMaster.objects.filter(pk=order_master.id).update(receiver=receiver,
                                                              phone=phone,
                                                              zip_code=zip_code,
                                                              address=address,
                                                              detail_address=detail_address,
                                                              delivery_request=delivery_request,
                                                              )

        OrderDetail.objects.filter(order_master=order_master).update(state="결제완료")

        # 스마터 머니 적립
        # reward_smarter_money(order_master)

        user = info.context.user

        # order_detail에 해당되는 product의 양을 빼주는 과정

        order_details = list(OrderDetail.objects.filter(order_master=order_master))
        products = {}

        for order_detail in order_details:
            product_id = str(order_detail.product_id)
            if product_id in products:
                products[product_id]['quantity'] += order_detail.quantity
            else:
                products[product_id] ={
                    'quantity': order_detail.quantity
                }

        for key, value in products.items():
            quantity = value['quantity']
            product = Product.objects.get(pk=int(key))
            Product.objects.filter(pk=int(key)).update(inventory_quantity=product.inventory_quantity-quantity)
            new_product = Product.objects.get(pk=int(key))

            if new_product.inventory_quantity <= 0:
                new_product.lack_inventory = True
                # send_notification(user=user, type="재고부족", product_names=new_product.name)
            else:
                new_product.lack_inventory = False
            new_product.save()
            for order_detail in order_details:
                ChangeHistory.objects.create(order_detail=order_detail,
                                             product_master=product.product_master,
                                             product=product,
                                             quantity_before=product.inventory_quantity,
                                             quantity_changed=-quantity,
                                             quantity_after=new_product.inventory_quantity,
                                             reason="판매")

        order_detail_drafts = OrderDetail.objects.filter(order_master=order_master, state="후작업중")
        belt_assign_work(order_details=order_detail_drafts)
        order_details = OrderDetail.objects.filter(order_master=order_master, state="출고준비")
        delivery(order_details=order_details)

        if smarter_money:
            wallet = user.wallet
            SmarterMoneyHistory.objects.create(
                order_master=order_master,
                history_number='U{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=wallet,
                transaction_type='사용',
                amount=smarter_money, description=order_master.order_name
            )
            wallet.balance -= smarter_money
            wallet.save()
        #send_notification(user=user, type="결제완료", order_master=order_master)

        return CompletePayment(success=True, order_master=order_master)

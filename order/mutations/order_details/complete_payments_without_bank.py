from datetime import datetime
import graphene
from django.db import transaction
from inventory.models import ChangeHistory
from order.methods.belt_assign_work import belt_assign_work
from order.models import OrderMaster
from order.models.order_detail import OrderDetail
from payment.models import PaymentSuccess, PaymentRequest
from product.models import Product


def change_state(order_master):
    payment_requests = PaymentRequest.objects.filter(orderId=order_master.order_number)
    if not payment_requests.exists():
        return
    payment_request = payment_requests.first()
    OrderDetail.objects.filter(order_master=order_master, state='무통장입금').update(state="결제완료")

    PaymentSuccess.objects.create(orderId=order_master.order_number,
                                  method=payment_request.method,
                                  requestedAt=datetime.now(),
                                  amount=payment_request.amount)

    # 스마터 머니 적립
    # reward_smarter_money(order_master)

    # order_detail에 해당되는 product의 양을 빼주는 과정

    order_details = list(OrderDetail.objects.filter(order_master=order_master, state='결제완료'))
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
            #send_notification(user=order_master.user, type="재고부족", product_names=new_product.name)
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


    # product = Product.objects.get(pk=int(key))
    # 해당 제품 보유량 0개일때 재고없음 표시
    # 재고가 0이어도 -로 주문 가능
    # if product.inventory_quantity == 0:
    #     Product.objects.filter(pk=int(key)).update(state="재고없음")

class CompletePaymentsWithoutBank(graphene.Mutation):

    class Arguments:
        order_master_numbers = graphene.List(graphene.String)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, order_master_numbers):

        for order_number in order_master_numbers:
            order_master = OrderMaster.objects.get(order_number=order_number)
            change_state(order_master)
            for child in order_master.children.all():
                change_state(child)

        return CompletePaymentsWithoutBank(success=True)
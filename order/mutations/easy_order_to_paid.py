from datetime import datetime

import graphene
from django.db import transaction

from order.models import OrderMaster
from order.models.order_detail import OrderDetail
from payment.models import PaymentRequest, PaymentSuccess


def change_state(order_number, order_master):
    requests = PaymentRequest.objects.filter(orderId=order_number)
    if requests.exists():
        requests.delete()

    payment_request = PaymentRequest.objects.create(method='무통장입금',
                                                    amount=order_master.price_to_pay,
                                                    orderId=order_master.order_number,
                                                    customerName=order_master.user.name,
                                                    orderName=order_master.order_name
                                                    )


    OrderDetail.objects.filter(order_master=order_master, state='간편주문').update(state="결제완료")

    PaymentSuccess.objects.create(orderId=order_master.order_number,
                                  method=payment_request.method,
                                  requestedAt=datetime.now(),
                                  amount=payment_request.amount)

class EasyOrderToPaid(graphene.Mutation):
    class Arguments:
        order_numbers= graphene.List(graphene.String)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __,
               order_numbers,
               ):
        for order_number in order_numbers:
            order_master = OrderMaster.objects.get(order_number=order_number)
            change_state(order_number, order_master)
            for child in order_master.children.all():
                change_state(child.order_number, child)

        return EasyOrderToPaid(success=True)

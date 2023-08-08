from datetime import datetime, timedelta

import graphene
from django.db import transaction

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from common.methods.get_bank_infos import get_bank_infos
from common.models import BankAccount
from cs.models import Coupon, CouponUseHistory
from order.models import OrderMaster
from order.models.order_detail import OrderDetail
from order.types.order_master_type import OrderMasterType
from payment.models import PaymentRequest
from smarter_money.models import SmarterMoneyHistory


class DepositWithoutAccount(graphene.Mutation):

    class Arguments:
        order_master_id = graphene.Int(required=True)
        receiver = graphene.String(required=True)
        phone = graphene.String(required=True)
        zip_code = graphene.String(required=True)
        address = graphene.String(required=True)
        detail_address = graphene.String()
        delivery_request = graphene.String()
        smarter_money = graphene.Int()
        coupon_id = graphene.Int()

    success = graphene.Boolean()
    order_master = graphene.Field(OrderMasterType)
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info,
               order_master_id,
               receiver,
               phone,
               zip_code,
               address,
               detail_address=None,
               delivery_request=None,
               smarter_money=None,
               coupon_id = None,
               ):

        user = info.context.user
        order_master = OrderMaster.objects.get(pk=order_master_id)

        OrderMaster.objects.filter(pk=order_master_id).update(receiver=receiver,
                                                              phone=phone,
                                                              zip_code=zip_code,
                                                              address=address,
                                                              detail_address=detail_address,
                                                              delivery_request=delivery_request,
                                                              )

        OrderDetail.objects.filter(order_master=order_master).update(state="무통장입금")
        if smarter_money:
            wallet = user.wallet
            SmarterMoneyHistory.objects.create(
                order_master=order_master,
                history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                wallet=wallet,
                transaction_type='사용',
                amount=smarter_money, description=order_master.order_name
            )
            wallet.balance -= smarter_money
            wallet.save()
        if coupon_id:
            now = datetime.now()
            coupon = Coupon.objects.get(pk=coupon_id)
            coupon.date_used = now
            coupon.save()
            order_master.coupon = coupon
            CouponUseHistory.objects.create(coupon=coupon,
                                            order_master=order_master,
                                            gym=coupon.user.gym,
                                            coupon_number=coupon.coupon_number,
                                            order_number=order_master.order_number,
                                            gym_name=coupon.user.gym.name,
                                            price=coupon.price,
                                            date_used=now)
        requests = PaymentRequest.objects.filter(orderId=order_master.order_number)
        if requests.exists():
            requests.delete()
        PaymentRequest.objects.create(method='무통장입금',
                                      amount=order_master.price_total + order_master.price_delivery,
                                      orderId=order_master.order_number,
                                      customerName=user.name,
                                      orderName=order_master.order_name
                                      )
        order_master.save()
        # send_notification(user=user, type="주문확인", order_master=order_master)
        return DepositWithoutAccount(success=True, order_master=order_master)

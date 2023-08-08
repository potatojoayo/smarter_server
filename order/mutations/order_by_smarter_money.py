from datetime import datetime

import graphene
from django.db import transaction
from cs.models import Coupon, CouponUseHistory
from order.models import OrderMaster, OrderDetail
from order.types.order_master_type import OrderMasterType
from payment.models import PaymentRequest, PaymentSuccess
from server.settings import logger
from smarter_money.models import SmarterMoneyHistory
from django.utils import timezone

class OrderBySmarterMoney(graphene.Mutation):
    class Arguments:
        order_master_id = graphene.Int(required=True)
        receiver = graphene.String(required=True)
        phone = graphene.String(required=True)
        zip_code = graphene.String(required=True)
        address = graphene.String(required=True)
        smarter_money = graphene.Int(required=True)
        detail_address = graphene.String()
        delivery_request = graphene.String()
        coupon_id = graphene.Int()

    success = graphene.Boolean()
    order_master = graphene.Field(OrderMasterType)
    message = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, order_master_id, receiver, phone, zip_code, address, smarter_money, detail_address=None,
               delivery_request=None, coupon_id=None):
        # try:
        logger.info('order_by_smarter_money')
        logger.info('order_master_id : '+str(order_master_id))
        user = info.context.user
        wallet = user.wallet
        order_master = OrderMaster.objects.get(pk=order_master_id)
        if wallet.balance < smarter_money :
            return OrderBySmarterMoney(success=False, order_master=order_master, message="스마터머니가 부족합니다.")
        coupon = Coupon.objects.get(pk=coupon_id) if coupon_id else None
        coupon_price = coupon.price if coupon else 0
        if order_master.price_to_pay != smarter_money + coupon_price:
            return OrderBySmarterMoney(success=False, order_master=order_master, message="스마터머니와 쿠폰 가격이 결제금액과 일치해야 주문이 진행됩니다.")
        if coupon:
            now = timezone.now()
            if coupon.start_of_use > now or coupon.end_of_use < now:
                return OrderBySmarterMoney(success=False, order_master=order_master, message="쿠폰의 유효기간은 확인해주세요.")
            coupon.date_used = now
            order_master.coupon = coupon
            CouponUseHistory.objects.create(coupon=coupon,
                                            order_master=order_master,
                                            gym=coupon.user.gym,
                                            coupon_number=coupon.coupon_number,
                                            order_number=order_master.order_number,
                                            gym_name=coupon.user.gym.name,
                                            price=coupon.price,
                                            date_used=now)
        order_master.receiver = receiver
        order_master.phone = phone
        order_master.zip_code = zip_code
        order_master.address = address
        order_master.detail_address = detail_address
        order_master.delivery_request = delivery_request

        OrderDetail.objects.filter(order_master=order_master).update(state="결제완료")

        SmarterMoneyHistory.objects.create(order_master=order_master,
                                           history_number='H{}{}'.format(user.phone, datetime.now().strftime('%y%m%d%H%M%S')),
                                           wallet=wallet,
                                           transaction_type="사용",
                                           amount=smarter_money, description=order_master.order_name + " 스마터머니 전체결제")
        wallet.balance -= smarter_money
        requests = PaymentRequest.objects.filter(orderId=order_master.order_number)
        if requests.exists():
            requests.delete()
        payment_request = PaymentRequest.objects.create(method='스마터머니',
                                                        amount=smarter_money,
                                                        orderId=order_master.order_number,
                                                        customerName=user.name,
                                                        orderName=order_master.order_name)
        PaymentSuccess.objects.create(orderId=payment_request.orderId,
                                      amount=smarter_money,
                                      requestedAt=datetime.now(),
                                      method='스마터머니',
                                      )
        wallet.save()
        order_master.save()
        if coupon_id:
            coupon.save()
        return OrderBySmarterMoney(success=True, order_master=order_master, message="결제 완료되었습니다.")
        # except Exception as e:
        #     print(e)
        #     logger.info('order_by_smarter_money')
        #     logger.info(e)
        #     return OrderBySmarterMoney(success=False, order_master=None, message="오류가 발생하였습니다.")



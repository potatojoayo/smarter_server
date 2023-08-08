import io
from base64 import b64encode
from datetime import datetime, timedelta

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from cs.models import Coupon, CouponUseHistory
from inventory.models import ChangeHistory
from order.methods.belt_assign_work import belt_assign_work
from order.methods.delivery import delivery
from order.models import OrderMaster, OrderDetail
from payment.models import PaymentRequest, PaymentSuccess, CancelSuccess
from payment.serializers.PaymentFailSerializer import PaymentFailSerializer
from payment.serializers.PaymentRequestSerializer import PaymentRequestSerializer
from payment.serializers.PaymentSuccessSerializer import PaymentSuccessSerializer
from product.models import Product
from server.settings import TOSS_SECRET_KEY, TOSS_CLIENT_KEY, MONEY_TOSS_CLIENT_KEY, MONEY_TOSS_SECRET_KEY
from smarter_money.models import SmarterMoneyHistory


def index(request):
    return render(request, 'payment/index.html')


def card(request):
    serializer = PaymentRequestSerializer(data=request.GET)
    if serializer.is_valid():
        old = PaymentRequest.objects.filter(orderId=serializer.validated_data['orderId'])
        if old.exists():
            old.delete()
        serializer.save()
    data = request.GET.dict()
    order_id = data['orderId']
    amount = data['amount']
    smarter_money = data.get('smarterMoney')
    if smarter_money and int(smarter_money) > amount:
        data['smarterMoney'] = amount
    data['client_key'] = TOSS_CLIENT_KEY
    if order_id[0] == 'S':
        data['client_key'] = MONEY_TOSS_CLIENT_KEY
        data['orderName'] = '스마터머니 충전'

    return render(request, 'payment/card.html',
                  data)


def transfer(request):
    serializer = PaymentRequestSerializer(data=request.GET)
    if serializer.is_valid():
        old = PaymentRequest.objects.filter(orderId=serializer.validated_data['orderId'])
        if old.exists():
            old.delete()
        serializer.save()
    data = request.GET.dict()
    data['client_key'] = TOSS_CLIENT_KEY
    return render(request, 'payment/transfer.html', data)


def success(request):
    try:
        data = request.GET.dict()
        order_id = data['orderId']
        amount = data['amount']
        smarter_money = int(data.get('smarterMoney')) if data.get('smarterMoney') else 0
        if smarter_money > amount:
            smarter_money = amount
        coupon = Coupon.objects.get(pk=int(data.get('couponId'))) if data.get('couponId') else None
        payment_request = PaymentRequest.objects.get(orderId=order_id, amount=amount)

        secret_key = TOSS_SECRET_KEY
        if order_id[0] == 'S':
            secret_key = MONEY_TOSS_SECRET_KEY
        url = "https://api.tosspayments.com/v1/payments/confirm"
        data = request.GET

        headers = {'Authorization': 'Basic {}'.format(b64encode(secret_key.encode('utf-8')).decode('utf-8')),
                   'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = JSONParser().parse(io.BytesIO(r.text.encode('utf-8')))

        if response_data.get('code') is not None:
            return render(request, 'payment/fail.html',
                          {"message": response_data.get('message'), "code": response_data.get('code'),
                           "orderId": request.GET.dict()['orderId']})
        else:
            serializer = PaymentSuccessSerializer(data=response_data)
            if serializer.is_valid(raise_exception=True):
                payment_success = serializer.save()
                payment_success.amount = data.dict()['amount']
                payment_success.save()
                if payment_success.easyPay is not None:
                    payment_success.method = '간편결제'
                    payment_request.method = '간편결제'
                    payment_request.save()
                    payment_success.save()

                order_master = OrderMaster.objects.get(order_number=order_id)
                order_details = order_master.details.all()
                order_details.update(state="결제완료")
                # reward_smarter_money(order_master)
                user = order_master.user
                products = {}

                for order_detail in order_details:
                    product_id = str(order_detail.product_id)
                    if product_id in products:
                        products[product_id]['quantity'] += order_detail.quantity
                    else:
                        products[product_id] = {
                            'quantity': order_detail.quantity
                        }

                for key, value in products.items():
                    quantity = value['quantity']
                    product = Product.objects.get(pk=int(key))
                    Product.objects.filter(pk=int(key)).update(inventory_quantity=product.inventory_quantity - quantity)
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
                    payment_success.amount += smarter_money
                    payment_success.save()
                    payment_request.amount += smarter_money
                    payment_request.save()
                    wallet.balance -= smarter_money
                    wallet.save()

                if coupon:
                    now = datetime.now()
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
                order_master.save()
            return render(request, 'payment/success.html',
                          request.GET.dict())

    except ObjectDoesNotExist:
        return render(request, 'payment/fail.html',
                      {"message": "주문 내역이 없습니다.", "code": "ObjectDoesNotExist",
                       "orderId": request.GET.dict()['orderId']})
    except ValidationError:
        return render(request, 'payment/fail.html',
                      {"message": "ValidationError", "code": "error", "orderId": request.GET.dict()['orderId']})
    except:
        return render(request, 'payment/fail.html',
                  {"message": "주문 내역이 없습니다.", "code": "ObjectDoesNotExist",
                   "orderId": request.GET.dict()['orderId']})


def fail(request):
    serializer = PaymentFailSerializer(data=request.GET)
    if serializer.is_valid():
        serializer.save()
    return render(request, 'payment/fail.html', request.GET.dict())


def cancel(request):
    try:
        data = request.GET
        order_id = data.dict()['orderId']
        payment_key = data.dict()['paymentKey']
        secret_key = TOSS_SECRET_KEY
        if order_id[0] == 'S':
            secret_key = MONEY_TOSS_SECRET_KEY

        url = "https://api.tosspayments.com/v1/payments/{}/cancel".format(data.dict()['paymentKey'])

        headers = {'Authorization': 'Basic {}'.format(b64encode(secret_key.encode('utf-8')).decode('utf-8')),
                   'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = JSONParser().parse(io.BytesIO(r.text.encode('utf-8')))
        print(response_data)

        if response_data.get('code') is not None:
            return render(request, 'payment/fail.html',
                          {"message": response_data.get('message'), "code": response_data.get('code'),
                           "orderId": request.GET.dict()['orderId']})

        payment_success = PaymentSuccess.objects.get(orderId=order_id, paymentKey=payment_key)

        for cancel_data in response_data['cancels']:
            print(cancel_data)
            CancelSuccess.objects.create(paymentSuccess=payment_success, **cancel_data)

    except ObjectDoesNotExist:
        return render(request, 'payment/fail.html',
                      {"message": "주문 내역이 없습니다.", "code": "ObjectDoesNotExist",
                       "orderId": request.GET.dict()['orderId']})
    except ValidationError:
        return render(request, 'payment/fail.html',
                      {"message": "ValidationError", "code": "error", "orderId": request.GET.dict()['orderId']})
    else:
        return render(request, 'payment/success.html',
                      request.GET.dict())


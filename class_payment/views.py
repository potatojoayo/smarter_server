import io
from base64 import b64encode
from datetime import datetime

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from class_payment.models import ClassPaymentRequest, ClassPaymentSuccess, ClassCancelSuccess, ClassPaymentMaster
from class_payment.serializers.ClassPaymentFailSerializer import ClassPaymentFailSerializer
from class_payment.serializers.ClassPaymentRequestSerializer import ClassPaymentRequestSerializer
from class_payment.serializers.ClassPaymentSuccessSerializer import ClassPaymentSuccessSerializer
from server.settings import CLASS_TOSS_SECRET_KEY, CLASS_TOSS_CLIENT_KEY


def class_index(request):
    return render(request, 'payment/class_index.html')


@transaction.atomic()
@csrf_exempt
def class_card(request):
    print("!!!!!")
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    # print("@@@@")
    # print(data)
    requests = data['requests']
    print(requests)
    order_ids = [r['orderId'] for r in requests]
    ClassPaymentRequest.objects.filter(orderId__in=order_ids).delete()
    serializer = ClassPaymentRequestSerializer(data=requests, many=True)
    if serializer.is_valid():
        serializer.save()
    ClassPaymentMaster.objects.filter(order_id__in=order_ids).update(
        payment_method=requests[0]['method'])

    total_amount = 0
    order_ids = []
    for r in requests:
        total_amount += int(r['amount'])
        order_ids.append(r['orderId'])
    post_data = {
        'client_key': CLASS_TOSS_CLIENT_KEY,
        'orderName': '학원비 결제',
        'orderId': requests[0]['orderId'],
        'customerName': requests[0]['customerName'],
        'amount': total_amount,
    }

    return render(request, 'payment/class_card.html',
                  post_data)


@transaction.atomic()
@csrf_exempt
def class_transfer(request):
    data = json.loads(request.body.decode('utf-8'))
    requests = data['requests']
    order_ids = [r['orderId'] for r in requests]
    ClassPaymentRequest.objects.filter(orderId__in=order_ids).delete()
    serializer = ClassPaymentRequestSerializer(data=requests, many=True)
    print("requests")
    print(requests)
    if serializer.is_valid():
        serializer.save()
    ClassPaymentMaster.objects.filter(order_id__in=order_ids).update(
        payment_method=requests[0]['method'])
    total_amount = 0
    order_ids = []
    for r in requests:
        total_amount += int(r['amount'])
        order_ids.append(r['orderId'])
    post_data = {
        'client_key': CLASS_TOSS_CLIENT_KEY,
        'orderName': '학원비 결제',
        'orderId': requests[0]['orderId'],
        'customerName': requests[0]['customerName'],
        'amount': total_amount,
        'bank': requests[0]['bank']
    }
    print(post_data)

    return render(request, 'payment/class_transfer.html',
                  post_data)


@transaction.atomic()
def class_success(request):

    print(request.GET)
    data = request.GET.dict()
    order_id = data['orderId']
    payment_master = ClassPaymentMaster.objects.get(order_id=order_id)
    payment_masters = ClassPaymentMaster.objects.filter(student=payment_master.student,
                                                        payment_status='미납',
                                                        payment_method=payment_master.payment_method
                                                        )
    order_ids = [p.order_id for p in payment_masters]
    payment_requests = ClassPaymentRequest.objects.filter(orderId__in=order_ids).order_by('id')

    secret_key = CLASS_TOSS_SECRET_KEY
    url = "https://api.tosspayments.com/v1/payments/confirm"
    data = request.GET

    headers = {'Authorization': 'Basic {}'.format(b64encode(secret_key.encode('utf-8')).decode('utf-8')),
               'Content-Type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    response_data = JSONParser().parse(io.BytesIO(r.text.encode('utf-8')))

    print(response_data.get('code'))
    print(response_data)
    if response_data.get('code') is not None:
        return render(request, 'payment/class_fail.html',
                      {"message": response_data.get('message'), "code": response_data.get('code'),
                       "orderId": request.GET.dict()['orderId']})
    else:
        serializer = ClassPaymentSuccessSerializer(data=response_data)
        print('페이먼트 석세스', serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            payment_success = serializer.save()
            for index, payment_request in enumerate(payment_requests):
                if index == 0:
                    continue
                payment_success.id = None
                payment_success.orderId = payment_request.orderId
                payment_success.amount = payment_request.amount
                payment_success.save()
                if payment_success.easyPay is not None:
                    payment_success.method = '간편결제'
                    payment_request.method = '간편결제'
                    payment_request.save()
                    payment_success.save()
        payment_masters.update(payment_status='납부완료', date_paid=datetime.now())

        return render(request, 'payment/class_success.html',
                      request.GET.dict())


def class_fail(request):
    serializer = ClassPaymentFailSerializer(data=request.GET)
    if serializer.is_valid():
        serializer.save()
    return render(request, 'payment/class_fail.html', request.GET.dict())


def class_cancel(request):
    try:
        data = request.GET
        order_id = data.dict()['orderId']
        payment_key = data.dict()['paymentKey']
        secret_key = CLASS_TOSS_SECRET_KEY

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

        class_payment_success = ClassPaymentSuccess.objects.get(orderId=order_id, paymentKey=payment_key)

        for cancel_data in response_data['cancels']:
            print(cancel_data)
            ClassCancelSuccess.objects.create(paymentSuccess=class_payment_success, **cancel_data)

    except ObjectDoesNotExist:
        return render(request, 'payment/class_fail.html',
                      {"message": "주문 내역이 없습니다.", "code": "ObjectDoesNotExist",
                       "orderId": request.GET.dict()['orderId']})
    except ValidationError:
        return render(request, 'payment/class_fail.html',
                      {"message": "ValidationError", "code": "error", "orderId": request.GET.dict()['orderId']})
    else:
        return render(request, 'payment/class_success.html',
                      request.GET.dict())


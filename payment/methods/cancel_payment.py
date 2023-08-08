import io
import json
from base64 import b64encode

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser

from payment.models import PaymentSuccess, CancelSuccess
from server.settings import TOSS_SECRET_KEY


def cancel_payment(order_number):
    try:
        payment_success = PaymentSuccess.objects.get(orderId=order_number)
        payment_key = payment_success.paymentKey
        data = {'cancelReason': "고객이 취소를 원함"}
        url = "https://api.tosspayments.com/v1/payments/{}/cancel".format(payment_key)
        headers = {'Authorization': 'Basic {}'.format(b64encode(TOSS_SECRET_KEY.encode('utf-8')).decode('utf-8')),
                   'Content-Type': 'application/json'}
        print(json.dumps(data))
        r = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = JSONParser().parse(io.BytesIO(r.text.encode('utf-8')))
        print(response_data)
        if response_data.get('code') is not None:
            return False
        payment_success = PaymentSuccess.objects.get(orderId=order_number, paymentKey=payment_key)
        for cancel_data in response_data['cancels']:
            print(cancel_data)
            CancelSuccess.objects.create(paymentSuccess=payment_success, **cancel_data)
        return True
    except ObjectDoesNotExist:
        return False

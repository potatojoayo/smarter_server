from rest_framework import serializers

from payment.models import CardSuccess, TransferSuccess
from payment.models.easypay_success import EasyPaySuccess
from payment.models.payment_success import PaymentSuccess
from payment.serializers.CardSuccessSerializer import CardSuccessSerializer
from payment.serializers.EasyPaySuccessSerializer import EasyPaySuccessSerializer
from payment.serializers.TransferSuccessSerializer import TransferSuccessSerializer


class PaymentSuccessSerializer(serializers.ModelSerializer):
    card = CardSuccessSerializer(required=False, allow_null=True)
    transfer = TransferSuccessSerializer(required=False, allow_null=True)
    easyPay = EasyPaySuccessSerializer(required=False, allow_null=True)

    class Meta:
        model = PaymentSuccess
        fields = '__all__'

    def create(self, validated_data):
        print('***validated_data:', validated_data)
        card_data = validated_data.pop('card')
        transfer_data = validated_data.pop('transfer')
        easy_pay_data = validated_data.pop('easyPay')
        if card_data is not None:
            card_success = CardSuccess.objects.create(**card_data)
            return PaymentSuccess.objects.create(card=card_success, **validated_data)
        elif transfer_data is not None:
            transfer_success = TransferSuccess.objects.create(**transfer_data)
            return PaymentSuccess.objects.create(transfer=transfer_success, **validated_data)
        elif easy_pay_data is not None:
            easy_pay_success = EasyPaySuccess.objects.create(**easy_pay_data)
            return PaymentSuccess.objects.create(easyPay=easy_pay_success, **validated_data)

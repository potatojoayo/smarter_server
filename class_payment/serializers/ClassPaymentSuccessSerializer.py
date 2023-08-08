from rest_framework import serializers

from class_payment.models import ClassPaymentSuccess, ClassCardSuccess, ClassEasyPaySuccess, ClassTransferSuccess
from class_payment.serializers.ClassCardSuccessSerializer import ClassCardSuccessSerializer
from class_payment.serializers.ClassEasyPaySuccessSerializer import ClassEasyPaySuccessSerializer
from class_payment.serializers.ClassTransferSuccessSerializer import ClassTransferSuccessSerializer


class ClassPaymentSuccessSerializer(serializers.ModelSerializer):
    card = ClassCardSuccessSerializer(required=False, allow_null=True)
    transfer = ClassTransferSuccessSerializer(required=False, allow_null=True)
    easyPay = ClassEasyPaySuccessSerializer(required=False, allow_null=True)

    class Meta:
        model = ClassPaymentSuccess
        fields = '__all__'

    def create(self, validated_data):
        print('***validated_data:', validated_data)
        card_data = validated_data.pop('card')
        transfer_data = validated_data.pop('transfer')
        easy_pay_data = validated_data.pop('easyPay')
        if card_data is not None:
            card_success = ClassCardSuccess.objects.create(**card_data)
            return ClassPaymentSuccess.objects.create(card=card_success, **validated_data)
        elif transfer_data is not None:
            transfer_success = ClassTransferSuccess.objects.create(**transfer_data)
            return ClassPaymentSuccess.objects.create(transfer=transfer_success, **validated_data)
        elif easy_pay_data is not None:
            easy_pay_success = ClassEasyPaySuccess.objects.create(**easy_pay_data)
            return ClassPaymentSuccess.objects.create(easyPay=easy_pay_success, **validated_data)

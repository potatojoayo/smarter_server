from rest_framework import serializers

from payment.models.payment_fail import PaymentFail
from payment.models.transfer_success import TransferSuccess


class TransferSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferSuccess
        fields = '__all__'

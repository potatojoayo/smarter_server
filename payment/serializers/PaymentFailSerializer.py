from rest_framework import serializers

from payment.models.payment_fail import PaymentFail


class PaymentFailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentFail
        fields = '__all__'

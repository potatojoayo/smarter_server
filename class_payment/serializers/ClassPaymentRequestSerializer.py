from rest_framework import serializers

from class_payment.models import ClassPaymentRequest


class ClassPaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassPaymentRequest
        fields = '__all__'

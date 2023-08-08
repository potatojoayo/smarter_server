from rest_framework import serializers

from class_payment.models import ClassPaymentFail


class ClassPaymentFailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassPaymentFail
        fields = '__all__'

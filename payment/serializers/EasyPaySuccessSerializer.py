from rest_framework import serializers

from payment.models.easypay_success import EasyPaySuccess


class EasyPaySuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = EasyPaySuccess
        fields = '__all__'

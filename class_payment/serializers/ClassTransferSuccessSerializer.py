from rest_framework import serializers

from class_payment.models import ClassTransferSuccess


class ClassTransferSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTransferSuccess
        fields = '__all__'

from rest_framework import serializers

from class_payment.models import ClassEasyPaySuccess


class ClassEasyPaySuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassEasyPaySuccess
        fields = '__all__'

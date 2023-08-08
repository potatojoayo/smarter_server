from rest_framework import serializers

from class_payment.models import ClassCardSuccess


class ClassCardSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCardSuccess
        fields = '__all__'

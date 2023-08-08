from rest_framework import serializers

from payment.models.card_success import CardSuccess


class CardSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardSuccess
        fields = '__all__'

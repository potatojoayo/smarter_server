from graphene_django import DjangoObjectType

from order.models import Payment


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment

from graphene_django import DjangoObjectType

from payment.models import PaymentRequest


class PaymentRequestType(DjangoObjectType):

    class Meta:
        model = PaymentRequest

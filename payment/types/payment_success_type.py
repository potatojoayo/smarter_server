from graphene_django import DjangoObjectType

from payment.models import PaymentSuccess


class PaymentSuccessType(DjangoObjectType):

    class Meta:
        model = PaymentSuccess

from graphene_django import DjangoObjectType

from common.models import BankAccount


class BankAccountType(DjangoObjectType):
    class Meta:
        model = BankAccount


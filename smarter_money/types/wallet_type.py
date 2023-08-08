import graphene
from graphene_django import DjangoObjectType

from smarter_money.models import Wallet


class WalletType(DjangoObjectType):

    class Meta:
        model = Wallet

    identification = graphene.String()
    gym_name = graphene.String()
    phone = graphene.String()
    total_charge_amount = graphene.Int()
    total_used_amount = graphene.Int()
    accumulative_amount = graphene.Int()
    @staticmethod
    def resolve_identification(root, __):
        return root.user.identification
    @staticmethod
    def resolve_gym_name(root, __):
        return root.user.gym.name
    @staticmethod
    def resolve_phone(root, __):
        return root.user.phone

    @staticmethod
    def resolve_total_charge_amount(root, __):
        print(root.history.filter(transaction_type="충전"))
        total_charge_amount = sum(root.history.filter(transaction_type="충전").values_list('amount', flat=True))
        return total_charge_amount

    @staticmethod
    def resolve_total_used_amount(root, __):
        total_used_amount = sum(root.history.filter(transaction_type="사용").values_list('amount', flat=True))
        return total_used_amount

    @staticmethod
    def resolve_accumulative_amount(root, __):
        accumulative_amount = sum(root.history.filter(transaction_type="적립").values_list('amount', flat=True))
        return accumulative_amount


import graphene

from common.models import BankAccount
from common.types.bank_input_type import BankInputType


class CreateOrUpdateBankAccount(graphene.Mutation):
    class Arguments:
        accounts = graphene.List(BankInputType)
        deleted_account_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, accounts, deleted_account_ids):
        for account in accounts:
            if account.id:
                BankAccount.objects.filter(pk=account.id).update(**account)

            else:
                BankAccount.objects.create(**account)

        for id in deleted_account_ids:
            BankAccount.objects.filter(pk=id).delete()

        return CreateOrUpdateBankAccount(success=True)

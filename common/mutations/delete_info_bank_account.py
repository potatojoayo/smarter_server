import graphene

from common.models import BankAccount


class DeleteInfoBankAccount(graphene.Mutation):
    class Arguments:
        bank_account_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, bank_account_id):
        BankAccount.objects.filter(pk=bank_account_id).delete()

        return DeleteInfoBankAccount(success=True)
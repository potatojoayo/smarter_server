import graphene


class GymBankAccountType(graphene.ObjectType):
    bank_name = graphene.String()
    bank_owner_name = graphene.String()
    bank_account_no = graphene.String()

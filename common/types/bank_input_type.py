import graphene
from graphene_file_upload.scalars import Upload


class BankInputType(graphene.InputObjectType):
    id = graphene.Int()
    bank_name = graphene.String()
    owner_name = graphene.String()
    account_no = graphene.String()
    is_default = graphene.Boolean()
    is_active = graphene.Boolean()

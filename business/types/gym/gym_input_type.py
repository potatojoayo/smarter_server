import graphene
from graphene_file_upload.scalars import Upload

from authentication.types.user_input_type import UserInputType


class GymInputType(graphene.InputObjectType):

    user = UserInputType()
    agency_id = graphene.Int()
    name = graphene.String()
    owner_name = graphene.String()
    email = graphene.String()
    memo = graphene.String()
    manager_name = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    zip_code = graphene.String()
    business_registration_number = graphene.String()
    business_registration_certificate = Upload()
    is_deduct_enabled = graphene.Boolean(default_value=False)
    refund_bank_name = graphene.String()
    refund_bank_owner_name = graphene.String()
    refund_bank_account_no = graphene.String()
    class_payment_bank_name = graphene.String()
    class_payment_bank_owner_name = graphene.String()
    class_payment_bank_account_no = graphene.String()

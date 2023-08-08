import graphene
from graphene_file_upload.scalars import Upload

from authentication.types.user_input_type import UserInputType


class AgencyInputType(graphene.InputObjectType):
    name = graphene.String()
    region = graphene.String()
    business_registration_number = graphene.String()
    business_registration_certificate = Upload()
    address = graphene.String()
    detail_address = graphene.String()
    id = graphene.Int()
    zip_code = graphene.String()
    user = UserInputType()
    email = graphene.String()
    memo = graphene.String()


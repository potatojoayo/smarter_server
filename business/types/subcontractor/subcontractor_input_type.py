import graphene

from graphene_file_upload.scalars import Upload

from authentication.types.user_input_type import UserInputType


class SubcontractorInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=True)
    business_registration_number = graphene.String()
    business_registration_certificate = Upload()
    address = graphene.String()
    zip_code = graphene.String()
    detail_address = graphene.String()
    user = UserInputType()

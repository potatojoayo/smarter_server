import graphene
from graphene_file_upload.scalars import Upload


class SupplierInputType(graphene.InputObjectType):

    id = graphene.Int()
    name = graphene.String()
    address = graphene.String()
    manager = graphene.String()
    phone = graphene.String()
    fax = graphene.String()
    email = graphene.String()
    business_registration_number = graphene.String()
    business_registration_certificate = Upload()


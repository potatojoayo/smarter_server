import graphene

class AddressInputType(graphene.InputObjectType):
    user_id = graphene.Int()
    name = graphene.String()
    receiver = graphene.String()
    phone = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    zip_code = graphene.String()
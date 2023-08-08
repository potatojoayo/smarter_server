import graphene


class OrderingUserInputType(graphene.InputObjectType):
    user_id = graphene.Int()
    receiver = graphene.String()
    zip_code = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    phone = graphene.String()

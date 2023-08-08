import graphene


class UserInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    identification = graphene.String()
    phone = graphene.String()
    password = graphene.String()
    is_active = graphene.Boolean()
    is_admin = graphene.Boolean()
    fcm_token = graphene.String()

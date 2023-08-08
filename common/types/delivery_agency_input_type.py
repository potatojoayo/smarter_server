import graphene


class DeliveryAgencyInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    is_default = graphene.Boolean()
    is_active = graphene.Boolean()

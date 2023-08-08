import graphene


class BrandInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=True)
    order = graphene.Int(default_value=-1)

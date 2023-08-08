import graphene


class CategoryInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=True)
    parent = graphene.Int(required=False)
    order = graphene.Int()
    depth = graphene.Int()
    children = graphene.List(lambda: CategoryInputType)

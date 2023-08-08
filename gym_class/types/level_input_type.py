import graphene


class LevelInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    belt = graphene.String()
    belt_color = graphene.String()
    belt_brand = graphene.String()

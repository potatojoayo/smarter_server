import graphene


class ClassMasterInputType(graphene.InputObjectType):
    id = graphene.Int()
    gym_id = graphene.Int()
    name = graphene.String(required=True)
    is_deleted = graphene.Boolean(default_value=False)


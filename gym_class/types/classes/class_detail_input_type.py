import graphene


class ClassDetailInputType(graphene.InputObjectType):
    hour_start = graphene.Int(required=True)
    min_start = graphene.Int(required=True)
    hour_end = graphene.Int(required=True)
    min_end = graphene.Int(required=True)
    is_deleted = graphene.Boolean(default_value=False)


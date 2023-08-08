import graphene


class DetailInputType(graphene.InputObjectType):
    detail_id = graphene.Int()
    quantity_received = graphene.Int()
    reason_not_received = graphene.String()



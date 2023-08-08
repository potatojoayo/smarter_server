import graphene


class CsRequestInputType(graphene.InputObjectType):
    order_master_id = graphene.Int()
    category = graphene.String()
    reason = graphene.String()

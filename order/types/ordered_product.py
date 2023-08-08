import graphene


class OrderedProductInputType(graphene.InputObjectType):
    product_master_id = graphene.Int()
    product_id = graphene.Int()
    quantity = graphene.Int()
    draft_id = graphene.Int()
    student_names = graphene.List(graphene.String)
    user_request = graphene.String()
    date_to_be_shipped = graphene.String()
    is_direct_delivery = graphene.Boolean()



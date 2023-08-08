import graphene


class TaOrderedProductInputType(graphene.InputObjectType):
    product_master_id = graphene.Int()
    product_id = graphene.Int()
    quantity = graphene.Int()
    draft_id = graphene.Int()
    student_names = graphene.List(graphene.String)
    user_request = graphene.String()



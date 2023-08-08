import graphene


class ProductInputType(graphene.InputObjectType):

    id = graphene.Int()
    product_master_id = graphene.Int()
    model_number = graphene.String(required=True)
    name = graphene.String(required=True)
    color = graphene.String(required=True)
    size = graphene.String(required=True)
    state = graphene.String(required=True)

    # 추가금
    price_additional = graphene.Int()

    # 재고관리
    inventory_quantity = graphene.Int()
    expected_inventory_quantity = graphene.Int()
    goal_inventory_quantity = graphene.Int()
    threshold_inventory_quantity = graphene.Int()

    # 삭제
    is_deleted = graphene.Boolean()

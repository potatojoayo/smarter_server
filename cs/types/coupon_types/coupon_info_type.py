import graphene


class CouponInfoType(graphene.ObjectType):
    total_users_count = graphene.Int()
    total_expected_price = graphene.Int()
    gym_ids = graphene.List(graphene.Int)
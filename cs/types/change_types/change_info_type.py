import graphene


class ChangeInfoType(graphene.ObjectType):
    changing_products_price = graphene.Int()
    total_delivery_price = graphene.Int()
    payment_amount = graphene.Int()
    current_smarter_money = graphene.Int()
    after_smarter_money = graphene.Int()
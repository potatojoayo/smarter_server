import graphene


class ProductStatisticType(graphene.ObjectType):

    brand = graphene.String()
    category = graphene.String()
    sub_category = graphene.String()
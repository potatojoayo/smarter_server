import graphene
from graphene import relay


class ProductStatisticsType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node, )
    brand_name = graphene.String()
    category_name = graphene.String()
    sub_category_name = graphene.String()
    product_name = graphene.String()
    amount = graphene.Int()
    date_from = graphene.String()
    date_to = graphene.String()

import graphene

from product.types.product_master.product_master_type import ProductMasterType


class ProductMastersType(graphene.ObjectType):

    product_masters = graphene.List(ProductMasterType)
    total_count = graphene.Int()

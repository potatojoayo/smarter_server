import graphene

from product.models import Brand
from product.types.brand.brand_type import BrandType
from product.types.brand.brand_input_type import BrandInputType


class UpdateBrand(graphene.Mutation):
    class Arguments:
        updating_brands = graphene.List(BrandInputType)
        deleting_brand_ids = graphene.List(graphene.Int)
    brands = graphene.List(BrandType)
    product_exists = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, updating_brands, deleting_brand_ids):

        for deleting_id in deleting_brand_ids:
            brand = Brand.objects.get(pk=deleting_id)
            products = brand.products
            if products.all().count() > 0:
                return UpdateBrand(product_exists=True)
            else:
                brand.delete()

        for updating_brand in updating_brands:
            print(updating_brand)

            # 새로 만드는 경우
            if updating_brand.id < 0:
                Brand.objects.create(name=updating_brand.name, order=updating_brand.order)

            # 업데이트 하는경우
            else:
                old_brand = Brand.objects.get(pk=updating_brand.id)
                old_brand.name = updating_brand.name
                old_brand.order = updating_brand.order
                old_brand.save()

        return UpdateBrand(brands=Brand.objects.all())











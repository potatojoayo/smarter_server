import graphene
from django.db import IntegrityError, transaction
from graphene_file_upload.scalars import Upload

from product.models import ProductMaster, Product, ProductImage, Draft, DraftImage, NewDraft, Category
from product.types import ProductMasterInputType
from product.types.product.product_input_type import ProductInputType
from product.types.product_master.product_master_type import ProductMasterType


class CreateOrUpdateProductMaster(graphene.Mutation):
    class Arguments:
        product_master = ProductMasterInputType()
        products = graphene.List(ProductInputType)
        new_images = graphene.List(Upload)
        deleted_image_ids = graphene.List(graphene.Int)

    product_master = graphene.Field(ProductMasterType)
    duplicated = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, product_master, products, new_images, deleted_image_ids):

        try:
            if product_master.id:
                ProductMaster.objects.filter(pk=product_master.id).update(**product_master)
                new_product_master = ProductMaster.objects.get(pk=product_master.id)
                if product_master.thumbnail:
                    new_product_master.thumbnail = product_master.thumbnail
                if product_master.description_image:
                    new_product_master.description_image = product_master.description_image
                new_product_master.save()
            else:
                new_product_master = ProductMaster.objects.create(**product_master)
        except IntegrityError:
            return CreateOrUpdateProductMaster(duplicated=True)

        for product in products:
            if product.id:
                Product.objects.filter(pk=product.id).update(**product)
            else:
                product["product_master_id"] = new_product_master.id
                Product.objects.create(**product)

        for image in new_images:
            ProductImage.objects.create(product_master=new_product_master, image=image)

        for deleted_image_id in deleted_image_ids:
            ProductImage.objects.filter(pk=deleted_image_id).delete()

        return CreateOrUpdateProductMaster(product_master=new_product_master)

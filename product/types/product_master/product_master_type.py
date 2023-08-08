import os
import graphene
from graphene_django import DjangoObjectType
from product.models import ProductMaster, NewDraft
from product.types.product_image.product_image_type import ProductImageType
from product.types.product.product_type import ProductType
from ..draft import DraftType
from product.models import Draft
from ..draft.new_draft_type import NewDraftType


class ProductMasterType(DjangoObjectType):
    class Meta:
        model = ProductMaster

    product_master_id = graphene.Int()
    images = graphene.List(ProductImageType)
    products = graphene.List(ProductType)
    thumbnail = graphene.String()
    description_image = graphene.String()
    drafts = graphene.List(NewDraftType, user_id=graphene.Int())
    colors = graphene.List(graphene.String)
    sizes = graphene.List(graphene.String)

    @staticmethod
    def resolve_colors(root, _):
        return root.colors

    @staticmethod
    def resolve_sizes(root, _):
        return root.sizes

    @staticmethod
    def resolve_product_master_id(root, _):
        return root.id

    @staticmethod
    def resolve_images(root, _):
        return root.images.all()

    @staticmethod
    def resolve_products(root, _):
        return root.products.filter(is_deleted=False)

    @staticmethod
    def resolve_thumbnail(root, info):
        return os.environ.get("BASE_URL")+root.thumbnail.url

    @staticmethod
    def resolve_description_image(root, info):
        if root.description_image:
            return os.environ.get("BASE_URL")+root.description_image.url

    @staticmethod
    def resolve_drafts(root, info, user_id):
        if user_id:
            return NewDraft.objects.filter(user_id=user_id, sub_category_id=root.sub_category.id, is_deleted=False)
        return NewDraft.objects.filter(user_id=info.context.user.id, sub_category_id=root.sub_category.id, is_deleted=False)

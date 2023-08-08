import os
import graphene
from graphene_django import DjangoObjectType

from product.models import Draft, NewDraft
from product.types.size.draft_size_type import DraftSizeType


class NewDraftType(DjangoObjectType):
    class Meta:
        model = NewDraft

    image = graphene.String()
    category_name = graphene.String()
    sub_category_name = graphene.String()
    sizes = graphene.List(DraftSizeType)
    @staticmethod
    def resolve_image(root, _):
        if root.image:
            return os.environ.get("BASE_URL") + root.image.url

    @staticmethod
    def resolve_category_name(root: NewDraft, _):
        return root.sub_category.parent.name

    @staticmethod
    def resolve_sub_category_name(root: NewDraft, _):
        return root.sub_category.name

    @staticmethod
    def resolve_sizes(root, _):
        print(111)
        print(root)
        return root.sizes.all().order_by('id')


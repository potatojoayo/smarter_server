from graphene_django import DjangoObjectType

from product.models.draft_size import DraftSize


class DraftSizeType(DjangoObjectType):
    class Meta:
        model = DraftSize
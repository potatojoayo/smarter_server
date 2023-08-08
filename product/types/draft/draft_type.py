import os
import graphene
from graphene_django import DjangoObjectType

from product.models import Draft


class DraftType(DjangoObjectType):
    class Meta:
        model = Draft

    image = graphene.String()
    
    @staticmethod
    def resolve_image(root, _):
        if root.draft_image:
            return os.environ.get("BASE_URL") + root.draft_image.image.url

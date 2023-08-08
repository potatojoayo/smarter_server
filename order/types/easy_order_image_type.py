import os

import graphene
from graphene_django import DjangoObjectType
from order.models import EasyOrderImage


class EasyOrderImageType(DjangoObjectType):
    class Meta:
        model = EasyOrderImage

    image = graphene.String()

    @staticmethod
    def resolve_image(root, _):
        return os.environ.get("BASE_URL")+root.image.url



import os
import graphene
from graphene_django import DjangoObjectType
from product.models import ProductImage


class ProductImageType(DjangoObjectType):

    url = graphene.String()

    @staticmethod
    def resolve_url(root, _):
        return os.environ.get("BASE_URL")+root.image.url

    class Meta:
        model = ProductImage

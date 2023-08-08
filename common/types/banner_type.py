import os

import graphene
from graphene_django import DjangoObjectType

from common.models.banner import Banner


class BannerType(DjangoObjectType):
    class Meta:
        model = Banner

    image = graphene.String()

    @staticmethod
    def resolve_image(root, _):
        return os.environ.get("BASE_URL")+root.image.url

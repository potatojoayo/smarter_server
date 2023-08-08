import os

import graphene
from graphene_django import DjangoObjectType
from order.models import EasyOrderFile


class EasyOrderFileType(DjangoObjectType):
    class Meta:
        model = EasyOrderFile

    file = graphene.String()

    @staticmethod
    def resolve_file(root, _):
        return os.environ.get("BASE_URL")+root.file.url



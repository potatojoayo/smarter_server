from graphene_django import DjangoObjectType

from product.models import DraftRequest


class DraftRequestType(DjangoObjectType):

    class Meta:
        model = DraftRequest

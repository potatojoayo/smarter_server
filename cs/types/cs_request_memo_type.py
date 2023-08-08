from graphene_django import DjangoObjectType

from cs.models import CsRequestMemos


class CsRequestMemoType(DjangoObjectType):
    class Meta:
        model = CsRequestMemos
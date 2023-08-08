import graphene
from graphene_django import DjangoObjectType

from cs.models import CsRequestContents


class CsRequestContentType(DjangoObjectType):
    class Meta:
        model = CsRequestContents

    cs_request_content_id = graphene.Int()
    replies = graphene.List(lambda:CsRequestContentType)
    @staticmethod
    def resolve_cs_request_content_id(root, __):
        return root.id


    @staticmethod
    def resolve_replies(root, __):
        return root.replies.filter(is_deleted=False)



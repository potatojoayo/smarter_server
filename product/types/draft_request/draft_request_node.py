import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from base_classes import CountableConnectionBase

from product.models import DraftRequest
from product.types.draft import DraftType
from product.types.draft.new_draft_type import NewDraftType


class DraftRequestNode(DjangoObjectType):

    class Meta:
        model = DraftRequest
        interfaces = (relay.Node, )
        filter_fields = {
            'state': ['exact']
        }
        connection_class = CountableConnectionBase

    draft_request_id = graphene.Int()
    drafts = graphene.List(NewDraftType)

    @staticmethod
    def resolve_draft_request_id(root, _):
        return root.id

    @staticmethod
    def resolve_drafts(root, _):
        return root.new_drafts.filter(is_deleted=False)

import graphene

from product.types.draft.new_draft_type import NewDraftType


class DraftsType(graphene.ObjectType):
    drafts = graphene.List(NewDraftType)
    total_count = graphene.Int()
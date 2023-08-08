import graphene
from graphene_file_upload.scalars import Upload


class WorkInputType(graphene.InputObjectType):

    id = graphene.Int()
    state = graphene.String()
    draft_image = Upload()

    belt_left_letter = graphene.String()
    belt_center_letter = graphene.String()
    belt_right_letter = graphene.String()


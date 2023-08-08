import graphene
from graphene_file_upload.scalars import Upload


class ChangeDisplayOrderInputType(graphene.InputObjectType):

    product_master_id = graphene.Int()
    display_order = graphene.Int()

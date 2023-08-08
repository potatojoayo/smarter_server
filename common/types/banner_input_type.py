import graphene
from graphene_file_upload.scalars import Upload


class BannerInputType(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()
    file = Upload()
    order = graphene.Int()

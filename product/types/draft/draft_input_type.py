import graphene
from graphene_file_upload.scalars import Upload


class DraftInputType(graphene.InputObjectType):
    product_master_id = graphene.Int()
    id = graphene.Int()
    image = graphene.String()
    file = Upload()
    price_work = graphene.Int(required=True)
    price_work_labor = graphene.Int(required=True)
    memo = graphene.String()
    font = graphene.String()
    thread_color = graphene.String()

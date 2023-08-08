import graphene
from graphene_file_upload.scalars import Upload


class ProductMasterInputType(graphene.InputObjectType):

    id = graphene.Int()
    product_number = graphene.String(required=True)
    name = graphene.String(required=True)
    category_id = graphene.Int(required=True)
    sub_category_id = graphene.Int(required=True)
    brand_id = graphene.Int(required=True)
    state = graphene.String(required=True)

    # 거래처
    supplier_id = graphene.Int(required=True)

    # 작업
    need_draft = graphene.Boolean(default_value=False)

    # 이미지
    thumbnail = Upload()
    description_image = Upload()

    # price
    price_consumer = graphene.Int(required=True)
    price_parent = graphene.Int(required=True)
    price_gym = graphene.Int(required=True)
    price_vendor = graphene.Int(required=True)

    # inventory
    goal_inventory_quantity = graphene.Int()
    threshold_inventory_quantity = graphene.Int()

    # delivery
    price_delivery = graphene.Int(required=True)
    delivery_type = graphene.String(required=True)
    max_quantity_per_box = graphene.Int()

    memo = graphene.String()

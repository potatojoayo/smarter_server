import graphene

from product.models import ProductMaster


class DeleteColor(graphene.Mutation):
    class Arguments:
        product_master_id = graphene.Int()
        deleting_color = graphene.String()

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, product_master_id,  deleting_color):
        try:
            product_master = ProductMaster.objects.get(pk=product_master_id)
            product_master.products.filter(color=deleting_color).update(is_deleted=True)
            return DeleteColor(success=True, message='색상이 삭제되었습니다.')
        except:
            return DeleteColor(success=False, message='오류가 발생하였습니다.')


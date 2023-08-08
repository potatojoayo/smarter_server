import graphene

from product.models import ProductMaster


class DeleteSize(graphene.Mutation):
    class Arguments:
        product_master_id = graphene.Int()
        deleting_size = graphene.String()

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, product_master_id,  deleting_size):
        try:
            product_master = ProductMaster.objects.get(pk=product_master_id)
            product_master.products.filter(size=deleting_size).update(is_deleted=True)
            return DeleteSize(success=True, message='사이즈가 삭제되었습니다.')
        except:
            return DeleteSize(success=False, message='오류가 발생하였습니다.')

